from django.test import TestCase
from .models import submission,question
from .tasks import execute
import json
from datetime import datetime
from .lang import langt
# Create your tests here.
class TasksTest(TestCase):
    def test_helloworld(self):
        self.question=question.objects.create(testcases=1)
        ws=submission.objects.create(
            q=self.question,
            lang='python3',
            code='print("hello")\nprint("world")'
            )
        ws.save()
        self.assertFalse(ws.done)
        execute(ws.id)
        ws.refresh_from_db()
        self.assertTrue(ws.done)
        jso=json.loads(ws.testresults)
        self.assertTrue(jso[0][1])

    
    def test_not_helloworld(self):
        self.question=question.objects.create(testcases=1)
        ws=submission.objects.create(
            q=self.question,
            lang='python3',
            code='print("hello")\nprint("orld")'
            )
        ws.save()
        self.assertFalse(ws.done)
        execute(ws.id)
        ws.refresh_from_db()
        self.assertTrue(ws.done)
        jso=json.loads(ws.testresults)
        self.assertFalse(jso[0][1])

    def test_infinite(self):
        self.question=question.objects.create(testcases=1)
        ws=submission.objects.create(
            q=self.question,
            lang='python3',
            code='while(True):\n\tpass'
            )
        ws.save()
        self.assertFalse(ws.done)
        execute(ws.id)
        ws.refresh_from_db()
        self.assertTrue(ws.done)
        jso=json.loads(ws.testresults)
        timetaken=datetime.strptime(jso[0][0],"%M:%S.%f")
        self.assertGreaterEqual(timetaken.second,langt["python3"])
        self.assertFalse(jso[0][1])
        
    def test_alreadydone(self):
        self.question=question.objects.create(testcases=1)
        ws=submission.objects.create(
            q=self.question,
            lang='python3',
            code='print("hello")\nprint("world")',
            done=True
            )
        ws.save()
        self.assertTrue(ws.done)
        execute(ws.id)
        ws.refresh_from_db()
        self.assertTrue(ws.done)
        self.assertEqual(ws.testresults,None)
    
    def test_alreadyexe(self):
        self.question=question.objects.create(testcases=1)
        ws=submission.objects.create(
            q=self.question,
            lang='python3',
            code='print("hello")\nprint("world")',
            cid=2
            )
        ws.save()
        self.assertFalse(ws.done)
        self.assertEqual(ws.cid,2)
        execute(ws.id)
        ws.refresh_from_db()
        self.assertGreater(ws.cid,0)
        self.assertEqual(ws.testresults,None)

    def test_compilation(self):
        self.question=question.objects.create(testcases=1)
        ws=submission.objects.create(
            q=self.question,
            lang='c',
            code='#include<stdio.h>\r\nint main(){prin("hello\\nworld\\n");}',
            )
        ws.save()
        self.assertFalse(ws.done)
        self.assertEqual(ws.cid,0)
        execute(ws.id)
        ws.refresh_from_db()
        self.assertTrue(ws.done)
        self.assertGreater(ws.cid,0)
        self.assertNotEqual(ws.errors,None)
        self.assertIsNone(ws.testresults)
    
    def test_customin(self):
        self.question=question.objects.create(testcases=1)
        ws=submission.objects.create(
            q=self.question,
            lang='python3',
            code='print(input())',
            customin="12"
            )
        ws.save()
        self.assertFalse(ws.done)
        self.assertEqual(ws.cid,0)
        execute(ws.id)
        ws.refresh_from_db()
        self.assertTrue(ws.done)
        self.assertGreater(ws.cid,0)
        jso=json.loads(ws.testresults)
        self.assertEqual(jso[0][1],'12\n')
    
    def test_fileaccess(self):
        self.question=question.objects.create(testcases=1)
        ws=submission.objects.create(
            q=self.question,
            lang='python3',
            code='a=open("../questions/1/output0.txt","r")\nres=a.read()\na.close()\nprint(res,end="")',
            )
        ws.save()
        self.assertFalse(ws.done)
        self.assertEqual(ws.cid,0)
        execute(ws.id)
        ws.refresh_from_db()
        self.assertTrue(ws.done)
        self.assertGreater(ws.cid,0)
        jso=json.loads(ws.testresults)
        self.assertFalse(jso[0][1])