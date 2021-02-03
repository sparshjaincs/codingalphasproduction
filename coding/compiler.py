import subprocess
import win32process, win32api, win32con
import time
class Compiler:
    '''
    Parameter:
    Compiler(language,sourcecode,testcase:List[List[]],solution:List[List[]],timelimit = 100)
    '''
    def __init__(self,language,sourcecode,testcase = [],solution=[],timelimit = 100):
        self.language = language
        self.code = sourcecode
        self.testcase = testcase
        self.solution = solution
        self.timelimit = timelimit
        self.status = ""
        self.passed = 0
        self.output = ""
        self.error = ""
        self.flag=0
        self.runtime = ""
        
    def language(self):
        return self.language
    def code(self):
        return self.code
    def testcase(self):
        return len(self.testcase)
    def testcase_text(self):
        return self.testcase
    def solution_text(self):
        return self.solution
    def status(self):
        return self.status
    def passed(self):
        return self.passed
    def output(self):
        return self.output
    def error(self):
        return self.error
    def write(self):
        if self.language == 'Python':
            ext = '.py'
        elif self.language == 'C':
            ext = '.c'
                
        else:
            self.flag = 1
            self.status = "Language Error"
            self.error = "Language doesn't exists!"
            self.runtime = "N/A ms"
            return 
        try:
                fp = open(f'test{ext}','w')
                fp.write(self.code)
                fp.close()
        except Exception as exp:
                self.flag=1
                self.error = str(exp)
                self.runtime = "N/A ms"
        
        return self.flag
    def pipeline(self):
        if self.language == 'Python':
            try:
                pipe = subprocess.Popen(['test.py'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
            except Exception as exp:
                self.flag = 1
                self.error = str(exp)
                self.runtime = 'N/A ms'
        elif self.language == 'C':
            try:
                pipe = subprocess.Popen(["C:\\MinGW\\bin\\g++.exe",'test.c'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
            except:
                self.flag = 1
                self.error = str(exp)
                self.runtime = 'N/A ms'
                
        else:
            pipe = ""
        return pipe
        
                
    def processinput(self,pipe):
        try:
            rt = time.time()
            for i in self.testcase:  # testcase[0][0] = testcasescount
                for j in i:
                    value = str(j) + '\n'
                    pipe.stdin.write(value)
                    pipe.stdin.flush()
            output,error = pipe.communicate()
            if error:
                self.flag = 1
                self.error = error
                self.status = 'Run Time Error'
                self.runtime = 'N/A ms'
                return {'flag':self.flag,'status':self.status,'error':self.error,'runtime':self.runtime}
            else:
                if output:
                    c = 0
                    flag = 0
                    tc = 0
                    if self.solution:
                        out = [eval(i) for i in output.split("\n")[:-1]]
                        
                        self.solution = [eval(i) for i in self.solution]
                        
                        for j in self.solution:
                            
                            if out[c] != j:
                                flag = 1
                                last = j
                                break
                            else:
                                tc+=1
                            c+=1
                        
                    rt = time.time() - rt
                    rt = round(rt*100)
                    if rt > self.timelimit:
                        self.flag = 1
                        self.status = "Time Limit Exceed"
                        self.error = "Time Complexity is Greater than given contraint."
                        self.runtime = str(rt)+'ms'
                        return {'flag':self.flag,'status':self.status,'error':self.error,'runtime':self.runtime}
                    self.passed = str(tc)
                    if flag:
                        self.flag = 0
                        self.status = 'Wrong Anwser'
                        self.output = output 
                        self.runtime = 'N/A ms'
                        
                    else:
                        self.flag = 0
                        self.status = 'Accepted'
                        self.output = output
                        self.runtime = str(rt) + " ms"
                        
                    return {'flag':self.flag,'status':self.status,'output':self.output,'runtime':self.runtime,'passed':self.passed}
                        
                    
                
        except Exception as exp:
            print(exp)
            self.flag = 1
            self.status = 'Run Time Error'
            self.error = str(exp)
            self.runtime ='N/A ms'
            return self.flag
    def process(self):
        ptr = self.write()
        if ptr == 0:
            pipeline = self.pipeline()
            if self.flag == 0:
                output = self.processinput(pipeline)
                if self.flag == 0:
                    return output
                    
                else:
                    return {'flag':self.flag,'status':self.status,'error':self.error,'runtime':self.runtime}
                
            else:
                return {'flag':self.flag,'status':self.status,'error':self.error,'runtime':self.runtime}
        else:
            return {'flag':self.flag,'status':self.status,'error':self.error,'runtime':self.runtime}
            
    
        
        