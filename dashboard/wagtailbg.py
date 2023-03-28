import dramatiq
from dramatiq.actor import Actor
from warnings import warn
from dramatiq.brokers.redis import RedisBroker
import django_dramatiq

class WagtailBackground:
    def __init__(self, name = "wagtail-background", broker = None) -> None:
        self.name = name
        self.broker = broker

    def enqueue(
        self,
        fn = None,
        *,
        actor_class = Actor,
        actor_name = None,
        queue_name  = "default",
        priority= 0,
        broker= None,
        args = (),
        kwargs = {},
        **options,
    ):
        """    
            Parameters:
            fn(callable): The function to wrap.
            actor_class(type): Type created by the decorator.  Defaults to
                :class:`Actor` but can be any callable as long as it returns an
                actor and takes the same arguments as the :class:`Actor` class.
            actor_name(str): The name of the actor.
            queue_name(str): The name of the queue to use.
            priority(int): The actor's global priority.  If two tasks have
                been pulled on a worker concurrently and one has a higher
                priority than the other then it will be processed first.
                Lower numbers represent higher priorities.
            broker(Broker): The broker to use with this actor.
            args = (): The positional arguments that are passed in send() method
            kwargs = {}: The keyword arguments that are passed in send() method
            **options: Arbitrary options that vary with the set of
                middleware that you use.  See ``get_broker().actor_options``.

            Returns:
            Actor: The decorated function.
        """
        if self.name is not None:
            warn(message="Wagtail Background already initialized")
        
        actor_name = fn.__name__
        broker = dramatiq.get_broker()

        actor = Actor(
            fn=fn, actor_name=actor_name, queue_name=queue_name,
            priority=priority, broker=broker, options=options
        )

        actor.send()
        print("Message Successfully Enqueued")


background = WagtailBackground(broker=RedisBroker(url = "redis://localhost:6379"))