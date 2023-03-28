from dramatiq.brokers.stub import StubBroker
import dramatiq.message
import traceback

class EagerBroker(StubBroker):
    def process_message(self, message):

        try:
            actor = self.get_actor(message.actor_name)

            # Adds pipeline support
            if 'pipe_target' in message.options:
                result = actor(*message.args, **message.kwargs)
                actor = self.get_actor(message.options['pipe_target']['actor_name'])
                if message.options['pipe_target']['options'].get('pipe_ignore', False):
                    extra_args = tuple()
                else:
                    extra_args = (result,)
                actor.send_with_options(
                    args=message.options['pipe_target']['args'] + extra_args,
                    kwargs=message.options['pipe_target']['kwargs'],
                    **message.options['pipe_target']['options']
                )
            else:
                actor(*message.args, **message.kwargs)
        except Exception as exc:
            traceback.print_exc(exc)

    def enqueue(self, message, *, delay=None):

        self.process_message(message)