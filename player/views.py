from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
import requests
import json

# Create your views here.
@never_cache
@login_required
def myPlayer(request,*args,**kwargs):
	return render(request, 'player/player.html',)


class PlayerView(TemplateView):
	template_name = "player/player.html"

	def get(self, request, *args, **kwargs):
		CHANNEL_ID = request.GET.get("urlChannel")
		YOUTUBE_API_KEY='AIzaSyCg2TiZUIkvSOqlNS0pVtAQG_0WkohscD0'
		queryset_list=[]
		vidID = []
		chName = []

		
		if CHANNEL_ID:
			YOUTUBE_URI = 'https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&part=snippet,id&type=video&order=date&maxResults=10'
			FORMAT_YOUTUBE_URI = YOUTUBE_URI.format( YOUTUBE_API_KEY, CHANNEL_ID)
			queryset_list.append(FORMAT_YOUTUBE_URI)
			content = requests.get(FORMAT_YOUTUBE_URI).text			
			data = json.loads(content)

			if not data.get('error'):
				for item in data.get('items'):
					id = item.get('id').get('videoId')
					chname = item.get('snippet').get('channelTitle')

					if id:
						#target="forVideo" - show in iframe forVideo
						id = '<a href="http://www.youtube.com/embed/'+id+'?autoplay=1" target="forVideo"><img src="https://i.ytimg.com/vi/'+id+'/default.jpg" width="120" height="90"></a>'
						vidID.append(id)
						#chName.append(chname)
				chName.append(chname)
			else:
				vidID = None
				chName = None

		else:
			queryset_list = None
		'''
		if CHANNEL_ID:
			try:
			    #create url with API-key
			    YOUTUBE_URI = 'https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&part=snippet,id&type=video&order=date&maxResults=10'
			    FORMAT_YOUTUBE_URI = YOUTUBE_URI.format( YOUTUBE_API_KEY, CHANNEL_ID)

			    #get json
			    content = requests.get(FORMAT_YOUTUBE_URI).text
			    data = json.loads(content)
			    
			    
			    
			    
			    for item in data.get('items'):
			        id = item.get('id').get('videoId')
			        chname = item.get('snippet').get('channelTitle')
			        
			        if id:
			            #target="forVideo" - show in iframe forVideo
			            id = '<a href="http://www.youtube.com/embed/'+id+'?autoplay=1" target="forVideo"><img src="https://i.ytimg.com/vi/'+id+'/default.jpg" width="120" height="90"></a>'
			            vidID.append(id)
			            chName.append(chname)
			    return vidID, chName
			except:
				return {}
		'''
		

		context = {
		           'video_list': vidID,
		           'name_list': chName,

		           }
		return render(request,self.template_name, context)