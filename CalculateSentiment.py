"""Created on Oct 21 2020@author: ashlychinnuvarghese, tincythomas"""from configparser import ConfigParserfrom ibm_watson import ToneAnalyzerV3# @UnresolvedImportfrom ibm_cloud_sdk_core.authenticators import IAMAuthenticator# @UnresolvedImportimport jsonclass CalculateSentiments:    def __init__(self):        configur = ConfigParser()        configur.read("config.ini")        self.__apikey = configur.get('toneanalyser','apikey')        self.__url = configur.get('toneanalyser','apiurl')        self.__authenticator = IAMAuthenticator(self.__apikey)        self.__toneAnalyser = ToneAnalyzerV3(version=configur.get('toneanalyser','apiversion'), authenticator=self.__authenticator)        self.__toneAnalyser.set_service_url(self.__url)        self.__analyticScore = 0;        self.__tentativeScore = 0;        self.__confidentScore = 0;        self.__joyScore = 0;        self.__sadnessScore = 0;        self.__fearScore = 0;        self.__angerScore = 0;    def __tweetEmotion(self,tweet):        response = self.__toneAnalyser.tone(tweet,content_type='text/plain')        #json_object = json.dumps(response.result)                        return response    def __calculateScores(self,response):        self.__analyticScore = 0;        self.__tentativeScore = 0;        self.__confidentScore = 0;        self.__joyScore = 0;        self.__sadnessScore = 0;        self.__fearScore = 0;        self.__angerScore = 0;        for row in response.result["document_tone"]["tones"]:            #print(row)                        if(row['tone_id']=='analytical'):                self.__analyticScore+=row['score']            if(row['tone_id']=='tentative'):                self.__tentativeScore+=row['score']            if(row['tone_id']=='confident'):                self.__confidentScore+=row['score']            if(row['tone_id']=='joy'):                self.__joyScore+=row['score']            if(row['tone_id']=='sadness'):                self.__sadnessScore+=row['score']            if(row['tone_id']=='fear'):                self.__fearScore+=row['score']            if(row['tone_id']=='anger'):                self.__angerScore+=row['score']    def getScoresforTweets(self,location,tweet):        data = {}        totalTweet = ''        for ind in tweet.index:            totalTweet += str(tweet['text'][ind])        response = self.__tweetEmotion(str(totalTweet).encode("utf-8"))        self.__calculateScores(response)        data =  {            "provinceName": location,            "analyticScore": round(self.__analyticScore*100, 0),            "tentativeScore": round(self.__tentativeScore*100, 0),            "confidentScore": round(self.__confidentScore*100, 0),            "joyScore": round(self.__joyScore*100, 0),            "sadnessScore": round(self.__sadnessScore*100, 0),            "fearScore": round(self.__fearScore*100, 0),            "angerScore": round(self.__angerScore*100, 0)        }        #print('Total tweets :',tweet.size)        #print('EMOTIONAL ANALYSIS')        #print('analyticScore :',round(self.__analyticScore*100, 0))        #print('tentativeScore :',round(self.__tentativeScore*100, 0))        #print('confidentScore :',round(self.__confidentScore*100, 0))        #print('joyScore :',round(self.__joyScore*100, 0))        #print('sadnessScore :',round(self.__sadnessScore*100, 0))        #print('fearScore :',round(self.__fearScore*100, 0))        #print('angerScore :',round(self.__angerScore*100, 0))        return  data    def getScoreForText(self,text):        data = {}        response = self.__tweetEmotion(str((text).encode("utf-8")))        self.__calculateScores(response)        data["text"] =  {            "type": "text",            "analyticScore": round(self.__analyticScore*100, 0),            "tentativeScore": round(self.__tentativeScore*100, 0),            "confidentScore": round(self.__confidentScore*100, 0),            "joyScore": round(self.__joyScore*100, 0),            "sadnessScore": round(self.__sadnessScore*100, 0),            "fearScore": round(self.__fearScore*100, 0),            "angerScore": round(self.__angerScore*100, 0)        }        return data                                                