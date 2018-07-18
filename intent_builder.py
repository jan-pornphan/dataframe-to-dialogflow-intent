import dialogflow_v2 as dialogflow
from dialogflow_v2.types import Context, Intent
from intent_helper import dataframe_to_intent
import sys


class IntentBuilder(object):

    def __init__(self, project_id, session_id):
        self.project_id = project_id
        self.session_id = session_id
        self.intents_client = dialogflow.IntentsClient()
        self.contexts_client = dialogflow.ContextsClient()
        self.parent = self.intents_client.project_agent_path(project_id)
        self.session_path = self.contexts_client.session_path(
            project_id, session_id)

    def create_intents(self, df):
        try:
            self.parent = self.intents_client.project_agent_path(
                self.project_id)
            self.session_path = self.contexts_client.session_path(
                self.project_id, self.session_id)
            self.df = df
            self.root_intents = df['root_intent'].unique()
            self._create_intent_recursive(self.root_intents, '', '', '', [])
            return self.list_intents()
        except:
            print("Unexpected error:", sys.exc_info())
            return

    def list_intents(self):
        intents = self.intents_client.list_intents(self.parent)
        return [intent.display_name for intent in intents]

    def delete_intents(self):
        intents = self.intents_client.list_intents(self.parent)
        for intent in intents:
            self.intents_client.delete_intent(intent.name)

    def _get_children(self, intent):
        children_df = self.df[(self.df.parent_intent == intent) &
                              (self.df.intent_name != intent)]
        return children_df['intent_name'].unique()

    def _create_intent_from_df(self,
                               intent_name,
                               intent_df,
                               root_id,
                               parent_id,
                               input_context,
                               output_context,
                               action):
        intent = dataframe_to_intent(
            intent_name, intent_df, root_id, parent_id, input_context, output_context, action)
        return self.intents_client.create_intent(self.parent, intent)

    def _create_output_contexts(self, context_id, lifespan_count):
        context_name = self.contexts_client.context_path(self.project_id,
                                                         self.session_id,
                                                         context_id)
        context = Context(name=context_name, lifespan_count=lifespan_count)
        output_context = self.contexts_client.create_context(self.session_path,
                                                             context)
        return [output_context]

    def _create_intent_recursive(self,
                                 intent_arr,
                                 root_id,
                                 parent_id,
                                 parent_action_name,
                                 parent_contexts):
        if len(intent_arr) == 0:
            return
        for intent_name in intent_arr:
            print('Creating ' + intent_name)
            children_intent = self._get_children(intent_name)

            # Set context
            input_context_names = [context.name for context in parent_contexts]
            context_name = intent_name + '-followup'
            output_contexts = []
            if len(children_intent) > 0:
                output_contexts = self._create_output_contexts(context_name, 2)

            # Create intent
            intent_df = self.df[self.df.intent_name == intent_name]
            if intent_name in self.root_intents:
                action = intent_name
                intent = self._create_intent_from_df(
                    intent_name, intent_df, '', '', input_context_names, output_contexts, action)
                root_id = intent.name  # change root id
            else:
                action = parent_action_name + '.' + intent_name
                intent = self._create_intent_from_df(
                    intent_name, intent_df, root_id, parent_id, input_context_names, output_contexts, action)

            self._create_intent_recursive(
                children_intent, root_id, intent.name, action, output_contexts)
