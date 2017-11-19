from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
import requests
import json
import re

# Create your views here.
@never_cache
@login_required
def myPlayer(request,*args,**kwargs):
	return render(request, 'player/player.html',)


class PlayerView(TemplateView):
	template_name = "player/player.html"

	def get(self, request, *args, **kwargs):
		CHANNEL_ID = request.GET.get("urlChannel")
		VIDEO_ID = None


		
		YOUTUBE_API_KEY='AIzaSyCg2TiZUIkvSOqlNS0pVtAQG_0WkohscD0'
		queryset_list=[]
		vidID = []
		chName = []
		
		match = re.search("=", CHANNEL_ID)
		if match:
			VIDEO_ID = CHANNEL_ID.rsplit('=', 1)[-1]
			CHANNEL_URI = 'https://www.googleapis.com/youtube/v3/videos?key={}&part=snippet&id={}'
			FORMAT_YOUTUBE_URI = CHANNEL_URI.format( YOUTUBE_API_KEY, VIDEO_ID)
			#get json
			content = requests.get(FORMAT_YOUTUBE_URI).text
			data = json.loads(content)

			#search ChannelId and ChannelTitle
			for item in data.get('items'):
				CHANNEL_ID = item.get('snippet').get('channelId')
		else:
			CHANNEL_ID = CHANNEL_ID.rsplit('/', 1)[-1]
		
		if CHANNEL_ID:
			
			YOUTUBE_URI = 'https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&part=snippet,id&type=video&order=date&maxResults=10'
			FORMAT_YOUTUBE_URI = YOUTUBE_URI.format( YOUTUBE_API_KEY, CHANNEL_ID)
			queryset_list.append(FORMAT_YOUTUBE_URI)
			content = requests.get(FORMAT_YOUTUBE_URI).text			
			data = json.loads(content)

			CHANNEL_ID = CHANNEL_ID.rsplit('=', 1)[-1]
			
			

			if not data.get('error'):
				for item in data.get('items'):
					id = item.get('id').get('videoId')
					chname = item.get('snippet').get('channelTitle')

					if id:
						#target="forVideo" - show in iframe forVideo
						#id = '<a href="https://www.youtube.com/embed/'+id+'?autoplay=1" target="forVideo"><img class="img-fluid mx-auto d-block" src="https://i.ytimg.com/vi/'+id+'/default.jpg"></a>'
						vidID.append(id)


				chName.append(chname)
			else:
				vidID = None
				chName = None

		else:

			queryset_list = None

		

		context = {
		           'video_list': vidID,
		           'name_list': chName,
		           
		           }
		return render(request,self.template_name, context)