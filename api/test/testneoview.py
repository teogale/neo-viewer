from django.test import TestCase
from neoview.views import Block, AnalogSignal, Segment, SpikeTrain
from rest_framework.test import APIRequestFactory
import json
import os


url_full_test_file = "https://github.com/teogale/test_file_api/raw/master/96711008.abf"
factory = APIRequestFactory()


class test_views(TestCase):

    def metadata_test(self,obj=None):
          # obj is a block or segment from neo
          # this method test common test for segment and block

          if obj==None:
               raise("obj parameter is none")

          else:
               # testing annotation data
               self.assertEqual(obj['annotations'],{'abf_version': '2.4'})

               #testing description
               self.assertEqual(obj['description'],'')

               # testing file_origin
               self.assertEqual(os.path.basename(obj['file_origin']),'96711008.abf')

               # testing name
               self.assertEqual(obj['name'],'')

               # testing rec_datetime only for block
               # self.assertEqual(obj['rec_datetime'],'1996-07-11T17:03:40')

               # testing file_name only for block
               # self.assertEqual(obj['file_name'],'96711008.abf')




    def test_get_block(self):
          # block made to test jsonresponse when reading a file with full given information
          # url parameter is required for block().get()

          # block number - 1
          # segment number - 16
          # contain only analog signal


          # block data   --- type
          # annotation   --- dictionnary
          # description  --- string
          # file_origin  --- string
          # name         --- string
          # rec_datetime --- string
          # file_name    --- string

          # segment data --- type
          # annotation   --- dictionnary
          # description  --- string
          # file_origin  --- string
          # rec_datetime --- string
          # name         --- string

          # irregularlysampledsignal --- list
          # analogsignals            --- list
          # spiketrains              --- list


          request = factory.get('blockdata/',{"url":url_full_test_file}, format='json')
          block = Block().get(request)
          json_data = json.loads(block.content)



          # testing the number of block
          number_of_block = len(json_data["block"])
          self.assertEqual(number_of_block, 1)

          # testing the number of segment
          number_of_segment = len(json_data["block"][0]['segments'])
          self.assertEqual(number_of_segment, 16)

          # testing rec_datetime
          self.assertEqual(json_data["block"][0]['rec_datetime'],'1996-07-11T17:03:40')

          # testing file_name
          self.assertEqual(os.path.basename(json_data["block"][0]['file_name']),'96711008.abf')

          # common test for block and segment
          self.metadata_test(obj=json_data['block'][0])
          for i in range(16):
               self.metadata_test(obj=json_data['block'][0]['segments'][i])

               # specific test for segment
               # test if irregularlysampledsignal is an empty list
               self.assertEqual(json_data["block"][0]['segments'][i]['irregularlysampledsignals'],[])
               # test if analogsignals is an empty list
               self.assertEqual(json_data["block"][0]['segments'][i]['analogsignals'],[])
               # test if spiketrains is an empty list
               self.assertEqual(json_data["block"][0]['segments'][i]['spiketrains'],[])

    def test_segment(self):

          # url && segment_id required for Segment().get()
          # segment data --- type
          # annotation   --- dictionnary
          # description  --- string
          # file_origin  --- string
          # rec_datetime --- string
          # name         --- string

          # irregularlysampledsignal --- list
          # analogsignals            --- list
          # spiketrains              --- list

          # segment composed of 2 analogsignal

          request = factory.get('segmentdata/',{"url":url_full_test_file, "segment_id":1}, format='json')
          segment = Segment().get(request)
          json_data = json.loads(segment.content)


          self.metadata_test(json_data)
            # test if irregularlysampledsignals is empty list
          self.assertEqual(json_data['irregularlysampledsignals'],[])
          # test if analogsignals contain 2 analogsignal
          self.assertEqual(json_data['analogsignals'],[{},{}])
          # test if spiketrains is an empty list
          self.assertEqual(json_data['spiketrains'],[])


    def test_get_analogsignal(self):

         # analogsignal require segment_id, analog_signal_id, down_sample_factor

         # analogsignal data --- type
         # t_start --- float
         # t_stop --- float
         # sampling_period --- float
         # values --- list
         # name --- string
         # time_dimensionality --- string
         # values_units --- string

         name = ['Chan0mV','AO#0']
         valueunit = ['mV','nA']
         for analogsignal_id in range(2):
          request = factory.get('analogsignaldata/',{"url":url_full_test_file,"segment_id":1,"analog_signal_id":analogsignal_id},format='json')
          analog_signal = AnalogSignal().get(request)
          json_data = json.loads(analog_signal.content)


          self.assertEqual(json_data['t_start'],4.0)
          self.assertEqual(json_data['t_stop'],4.7168)
          self.assertEqual(json_data['sampling_period'],0.0001)
          # not tested values
          self.assertEqual(json_data['name'],name[analogsignal_id])
          self.assertEqual(json_data['times_dimensionality'],'s')

          self.assertEqual(json_data['values_units'],valueunit[analogsignal_id])

    def test_spriketrain(self):

          # compose of 1 segment
          # 19 spiketrain
          # units --- float
          # t_stop --- float
          # times --- list
          # to test spiketrain an other file is needed as 96711008.abf doesnt contain one

          test_file = "https://drive.humanbrainproject.eu/f/076de9c19e0c4447a95e/?dl=1"

          request = factory.get('spiketraindata/',{"url":test_file,'segment_id':0, 'type': 'NixIO'}, format='json')
          spiketrain = SpikeTrain().get(request)
          json_data = json.loads(spiketrain.content)
          container = ["units","t_stop","times"]

          for i in range(20):
                for x in container:
                   self.assertEqual(x in json_data[str(i)],True)





    def test_get_block_missing_param(self):

           # block made to test jsonresponse when missing requirement
           # url parameter(string) is required for block().get()

           # missing url test
           request = factory.get('blockdata/',{}, format='json')
           block = Block().get(request)
           json_data = json.loads(block.content)
           self.assertEqual(json_data,{'error': 'URL parameter is missing','message': ''})


    def test_get_segment_missing_param(self):
           # test for missing requirement in segment
           # url parameter(string) is requirement for segment().get()
           # segment_id --- int

           # missing url test
           request = factory.get('segmentdata/',{}, format='json')
           segment = Segment().get(request)
           json_data = json.loads(segment.content)
           self.assertEqual(json_data,{'error': 'URL parameter is missing','message': ''})

           # missing segment_id
           request = factory.get('segmentdata/',{"url":url_full_test_file}, format='json')
           segment = Segment().get(request)
           json_data = json.loads(segment.content)
           self.assertEqual(json_data,{'error': 'segment_id parameter is missing','message': ''})

           # index_error segment_id
           request = factory.get('segmentdata/',{"url":url_full_test_file,"segment_id":18}, format='json')
           segment = Segment().get(request)
           json_data = json.loads(segment.content)
           self.assertEqual(json_data,{'error': 'IndexError on segment_id','message': ''})



    def test_get_analogsignal_missing_param(self):

           # test for missing requirement in analogsignal
           # url parameter(string) is requirement for analogsignal().get()
           # segment_id --- int
           # analog_signal_id --- int
           # downsamplingfactor --- int

           # missing url test
           request = factory.get('analogsignaldata/',{}, format='json')
           analogsignal = AnalogSignal().get(request)
           json_data = json.loads(analogsignal.content)
           self.assertEqual(json_data,{'error': 'URL parameter is missing','message': ''})

           # missing segment_id
           request = factory.get('analogsignaldata/',{"url":url_full_test_file}, format='json')
           analogsignal = AnalogSignal().get(request)
           json_data = json.loads(analogsignal.content)
           self.assertEqual(json_data,{'error': 'segment_id parameter is missing','message': ''})

           # missing analog_signal_id
           request = factory.get('analogsignaldata/',{"url":url_full_test_file,"segment_id":1}, format='json')
           analogsignal = AnalogSignal().get(request)
           json_data = json.loads(analogsignal.content)
           self.assertEqual(json_data,{'error': 'analog_signal_id parameter is missing','message': ''})

           # index_error segment_id
           request = factory.get('analogsignaldata/',{"url":url_full_test_file,"segment_id":18,"analog_signal_id":1}, format='json')
           analogsignal = AnalogSignal().get(request)
           json_data = json.loads(analogsignal.content)

           self.assertEqual(json_data,{'error': 'IndexError on segment_id','message': ''})


    def test_get_spriketrain_missing_param(self):

          test_file = "https://drive.humanbrainproject.eu/f/076de9c19e0c4447a95e/?dl=1"

          # test for missing url
          request = factory.get('spiketraindata/',{}, format='json')
          spiketrain = SpikeTrain().get(request)
          json_data = json.loads(spiketrain.content)
          self.assertEqual(json_data,{'error': 'URL parameter is missing','message': ''})


          #test for missing segment_id
          request = factory.get('spiketraindata/',{'url':test_file, 'type': 'NixIO'}, format='json')
          spiketrain = SpikeTrain().get(request)
          json_data = json.loads(spiketrain.content)
          self.assertEqual(json_data,{'error': 'segment_id parameter is missing','message': ''})

          #test for indexerror on segment_id
          request = factory.get('spiketraindata/',{'url':test_file,'segment_id':2, 'type': 'NixIO'}, format='json')
          spiketrain = SpikeTrain().get(request)
          json_data = json.loads(spiketrain.content)
          self.assertEqual(json_data,{'error': 'IndexError on segment_id','message': ''})
