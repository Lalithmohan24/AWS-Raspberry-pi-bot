import RPi.GPIO as GPIO
import boto3
import os,sys
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
TRIG = 17
ECHO = 27
m11 = 5
m12 = 6
m21 = 13
m22 = 19
count=0

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(m11,GPIO.OUT)
GPIO.setup(m12,GPIO.OUT)
GPIO.setup(m21,GPIO.OUT)
GPIO.setup(m22,GPIO.OUT)

#class target_robot():

def stop():
    GPIO.output(m11,0)
    GPIO.output(m12,0)
    GPIO.output(m21,0)
    GPIO.output(m22,0)
    print('stop')

def forward():
    GPIO.output(m11,1)
    GPIO.output(m12,0)
    GPIO.output(m21,1)
    GPIO.output(m22,0)      

def left():
    GPIO.output(m11,0)
    GPIO.output(m12,0)
    GPIO.output(m21,1)
    GPIO.output(m22,0)

def right():
    GPIO.output(m11,1)
    GPIO.output(m12,0)
    GPIO.output(m21,0)
    GPIO.output(m22,0)

def back():
    GPIO.output(m11,0)
    GPIO.output(m12,1)
    GPIO.output(m21,0)
    GPIO.output(m22,1)

def rightstop():
    GPIO.output(m11,1)
    GPIO.output(m12,0)
    GPIO.output(m21,0)
    GPIO.output(m22,0)

    time.sleep(0.5)

    GPIO.output(m11,0)
    GPIO.output(m12,0)
    GPIO.output(m21,0)
    GPIO.output(m22,0)

while True:
  print("list")
  print("1.Create collection")
  print("2.Add faces in the collection")
  print("3.Delete collection")
  print("4.Execute Programe..")
  print("5.exit")

  ans = int(input())

  print("")

  if ans == 1:
    print("Enter collection ID")
#    id = input()
    maxResults = 2
    collectionId = str(input())
    
    client = boto3.client('rekognition')
    print('Creating collection:' + collectionId)
    response=client.create_collection(CollectionId=collectionId)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')

  elif ans  == 2:

    print("Enter your collection id name")
    idname = str(input())
    
    print('wait')
    time.sleep(0.5)
    print("THREE")
    time.sleep(0.5)
    print("TWO")
    time.sleep(0.5)
    print("ONE")
    time.sleep(0.5)
    print("Take Picture")

    os.system("fswebcam -r 1024x720 --no-banner -S 10 --set brightness=100 /home/pi/webcam/source.jpeg")

    s3 = boto3.client('s3')
    bucket = 'youcode'
    file_name = '/home/pi/webcam/source.jpeg'
    key_name = 'source_image'
    s3.upload_file(file_name, bucket, key_name)

    print("Image uploaded S3 bucket successfully..")


    bucket='youcode'

    collectionId=idname

    photo='sourceimg.jpg'

    client=boto3.client('rekognition')

    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                ExternalImageId=photo,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])

    print('Results for ' + photo)
    print('Faces indexed:')

    try:

       for faceRecord in response['FaceRecords']:
           print('  Face ID: ' + faceRecord['Face']['FaceId'])
           print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    except:

       print('Faces not indexed:')
       for unindexedFace in response['UnindexedFaces']:
           print(' Location: {}'.format(unindexedFace['FaceDetail']['Boundingbox']))
           print(' Reasons:')
           for reason in unindexedFace['Reasons']:
               print('   ' + reason)


  elif ans == 3:
    print("Enter Delete Collection ID Name:")
    dltcollection = str(input())
    client = boto3.client('rekognition')
    response = client.delete_collection(CollectionId=dltcollection)
    print(response)
    print("collection deleted..")

  elif ans == 4:

    def searchFace():

       try:
          print("Enter your Collection Name:")
          name = str(input())
          bucket='youcode'
          collectionId=name
          fileName='/home/pi/webcam/sourceimg.jpg'
          threshold = 70
          maxFaces = 1

          client=boto3.client('rekognition')

          image_file = open(fileName, 'rb')

          response=client.search_faces_by_image(CollectionId=collectionId,
                                  Image={'Bytes': image_file.read()},
                                  FaceMatchThreshold=threshold,
                                  MaxFaces=maxFaces)

          faceMatches=response['FaceMatches']
#        print ('Matching Faces')
          for match in faceMatches:

              similar = int(match['Similarity'])
              if similar >= 70:
                 GPIO.output(TRIG, False)                 #Set TRIG as LOW
                 time.sleep(0.1)                                   #Delay
                 GPIO.output(TRIG, True)                  #Set TRIG as HI$
                 time.sleep(0.00001)                           #Delay of $
                 GPIO.output(TRIG, False)                 #Set TRIG as LOW
                 while GPIO.input(ECHO)==0:              #Check whether t$
                     pulse_start = time.time()
                 while GPIO.input(ECHO)==1:              #Check whether t$
                     pulse_end = time.time()
                 pulse_duration2 = pulse_end - pulse_start #time to get b$
                 target = pulse_duration2 * 17150        #Multiply pulse $
                 target = int(target)                 #Round to two decim$
                 print(target)
                 if target  >= 0:
                     print('Faces matching...')
                     print(similar)
                     print('Forward')
                     forward()
                     time.sleep(1)
                     stop()
                     time.sleep(1)

              elif similar > 50 and similar < 69:
                 print('Face not matching...')
                 print('Searching Face..')
                 right()
                 time.sleep(0.5)
                 stop()
                 time.sleep(0.5)
       except:
          print('NO faces in the image...')
          rightstop()
          time.sleep(1)

    while True:
        try:
           i=0
           avgDistance=0
           for i in range(5):
               GPIO.output(TRIG, False)                 #Set TRIG as LOW
               time.sleep(0.1)                                   #Delay
               GPIO.output(TRIG, True)                  #Set TRIG as HIGH
               time.sleep(0.00001)                           #Delay of 0.000$
               GPIO.output(TRIG, False)                 #Set TRIG as LOW
               while GPIO.input(ECHO)==0:              #Check whether the EC$
                   pulse_start = time.time()
               while GPIO.input(ECHO)==1:              #Check whether the EC$
                   pulse_end = time.time()
               pulse_duration1 = pulse_end - pulse_start #time to get back t$
               distance = pulse_duration1 * 17150        #Multiply pulse dur$
               distance = round(distance,2)                 #Round to two de$
               avgDistance=avgDistance+distance
               avgDistance=avgDistance/5
               print(avgDistance)
               flag=0
               if avgDistance < 15:      #Check whether the distance is with$
                  count=count+1
                  stop()
                  time.sleep(1)
                  back()
                  time.sleep(1.5)
                  time.sleep(1.5)
                  if (count%3 ==1) & (flag==0):
                     right()
                     flag=1
                  else:
                     left()
                     flag=0
                     time.sleep(1.5)
                     stop()
                     time.sleep(1)
               else:
                  flag=0
                  os.system("fswebcam -r 1024x720 --no-banner -S 10 --set brightness=100 /home/pi/source_img.jpg")
                  searchFace()
#           time.sleep(1)
                  time.sleep(0.5)

        except KeyboardInterrupt:

           print('keyboard interrupted')
            
  elif a  == 5:
    os.system(exit())
    print("exit")








