"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Event, Gamer


class EventView(ViewSet):
    """Level up event types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event type

        Returns:
            Response -- JSON serialized event type
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of event types
        """

        events = []

        # if request.event.:
        #   events = Event.objects.all()

        if "game" in request.query_params:
            try:
                game = Game.objects.get(pk=request.query_params["game"])
            except Game.DoesNotExist:
                return Response(
                    {"message": "An invalid game id was provided"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            events = Event.objects.filter(game__id=request.query_params["game"])

        else:
            events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handles the POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        game = Game.objects.get(pk=request.data["game"])
        # Generated from the Authorization Token
        organizer = Gamer.objects.get(user=request.auth.user)

        event = Event.objects.create(
            game=game,
            organizer = organizer,
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
        )

        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    
    def update(self, request, pk=None):
        """Handle PUT requests for an event
        
        Returns:
            Response -- Empty body with 204 status code
        """
        #Select the target Event using the pk (primary key)
        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""

    # The Meta class holds the configuration for the serializer.abs
    # We're telling the serializer to use the GameType model and to include
    #   the id and label fields
    class Meta:
        model = Event
        fields = ("id", "game", "description", "date", "time", "organizer")
