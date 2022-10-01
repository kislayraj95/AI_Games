import random

class FileManager:
    def __init__(self):
        self.UserFile="User.txt"
        self.EmployeeFile="Employee.txt"
    def LoginUser(self,name,password):
        """
        Function for user login 
        """
        file = ""
        try:
            file = open(self.UserFile)
        except: 
            print("File : "+self.UserFile+" does not exist")
            return
        data = file.read().split("\n")
        for row in data:
            if name+"\t"+password in row:
                record = row.split("\t")
                return int(record[0])
        else:
            print("User is not registered")
            return -1
    def RegisterNewUser(self,name,password,address,email,mob):
        "Function to add new user "
        file = open(self.UserFile)
        data = file.read().split("\n")
        file.close()
        if len(data)==1:
            data=[]
        for record  in data:
            if name+"\t"+password+"\t"+email in record:
                return "Already Registered "
        else:
            ID  = len(data)+10000   
            data.append(str(ID)+"\t"+name+"\t"+password+"\t"+email+'\t'+address+'\t'+mob)
            file = open(self.UserFile,"w")
            for i in data:
                file.write(i+'\n')
            file.close() 
            return "Successfully Registered"
    def AddEmployee(self,Empdata):
        """Add employee to file """
        try :
            file = open("Employee.txt","a")
            file.write(str(Empdata)+'\n')
            file.close()
        except: 
            print("File : "+self.EmployeeFile+" does not exist")
            return
    def GetSEDateSalary(self,sdate,edate,ID):
        """Function get salary detail between two given dates"""
        lst = []
        file = ""
        try :
            file = open(self.EmployeeFile,'r')
        except: 
            print("File : "+self.UserFile+" does not exist")
            return 
        data = file.read().split("\n")
        dat = ""
        for rowIndex in range(len(data)):
            r = data[rowIndex].split('\t')
            if data[rowIndex]=='':
                continue
            elif int(r[0])==ID and r[2]==sdate:
                lst.append(data[rowIndex].split('\t'))
            elif int(r[0])==ID and r[3]==edate:
                lst.append(data[rowIndex].split('\t'))
                file.close()
                return lst        
        file.close()
        return lst
        
        
    def RemoveEmployee(self,EmpID):
        """Remove emploee with ID EmpID"""
        file = ""
        try :
            file = open(self.UserFile,'r')
        except: 
            print("File : "+self.UserFile+" does not exist")
            return 
        isFound=False
        data = file.read().split("\n")
        for rowIndex in range(len(data)):
            r = data[rowIndex].split('\t')
            if data[rowIndex]=='':
                continue
            if int(r[0])==EmpID:
                data.pop(rowIndex)
                file.close()
                file = open(self.UserFile,'w')
                for record in data:
                    file.write(record+"\n")
                file.close()
                isFound=True
                break
        if isFound:
            print("Successfully removed")
        else:
            print("Employee not found")
    def getUserInfo(self, ID):
        """To get user information """
        file = ""
        try :
            file = open(self.UserFile,'r')
        except: 
            print("File : "+self.UserFile+" does not exist")
            return 
        data = file.read().split("\n")
        dat = ""
        for rowIndex in range(len(data)):
            r = data[rowIndex].split('\t')
            if data[rowIndex]=='':
                continue
            elif int(r[0])==ID:
                dat = data[rowIndex].split('\t')
                break
        file.close()
        
        try :
            file = open(self.EmployeeFile,'r')
        except: 
            print("File : "+self.EmployeeFile+" does not exist")
            return
        data = file.read().split("\n")
        emp = ""
        for rowIndex in range(len(data)):
            r = data[rowIndex].split('\t')
            if data[rowIndex]=='':
                continue
            elif int(r[0])==ID:
                emp = data[rowIndex].split('\t')
                break
        file.close()
        return dat,emp
        
    def getAllUserInfo(self):
        file = ""
        try :
            file = open(self.UserFile,'r')
            data = file.read().split('\n')
            file.close()
            return data
        except: 
            print("File : "+self.UserFile+" does not exist")
            return 
class user:
    def __init__(self,name="",password="",address="",email="",mob=""):
        self.name = name
        self.password = password
        self.address = address
        self.email =email
        self. mobile  =mob
        self.Filemanager = FileManager()
    def RegisterUser(self):
        self.Filemanager.RegisterNewUser(self.name,self.password,self.address,self.email,self.mobile)
    def setName(self, name):
        self.name=name
    def setPassword(self, password):
        self.passwrod=password
    def Login(self):
        ID = self.Filemanager.LoginUser(self.name,self.password)
        if ID ==-1:
            print("User does not exist, please contact our company")
            return -1
        else:
            return ID
class BankInfo:
    def __init__(self,bank_name="",branch_name="",account_number=""):
        self.bank_name=bank_name
        self.branch_name=branch_name
        self.account_number=account_number
    def __str__(self):
        return self.bank_name+"\t"+self.branch_name+"\t"+str(self.account_number)
class Department:
    def __init__(self,name="Information Technology",estab_year="1990",deptID="IT90"):
        self.name=name
        self.Established_year=estab_year
        self.deptID=deptID
    def __str__(self):
        return self.name+"__"+self.Established_year+"__"+self.deptID
    
class Employee(user):
    def __init__(self, basic_salary=100,housing_allowance=0, children_allowance=0, social_allowance=0,
                 transportation_allowance=0, Emirati_pension=0.05, car_loan=0, house_loan=0):
        user.__init__(self)
        self.housing_allowance=housing_allowance
        self.file_mang = FileManager()
        self.children_allowance=children_allowance 
        self.social_allowance=social_allowance
        self.transportation_allowance=transportation_allowance 
        self.Emirati_pension=transportation_allowance
        self.car_loan=car_loan
        self.house_loan=house_loan
        self.basic_salary =basic_salary
        self.net_salary=basic_salary+housing_allowance+children_allowance+social_allowance+transportation_allowance
        # Calculated the positive salary
        self.net_salary-=(Emirati_pension+car_loan+house_loan)*basic_salary
        # Deducation is done here
        self.EmpID=10000
    def CalculateNetPay(self):
        self.net_salary=basic_salary+house_allowance+children_allowance+social_allowance+transportation_allowance
        # Calculated the positive salary
        self.net_salary-=(Emirati_pension+car_loan+house_loan)*basic_salary
        # Deducation is done here
    def setDepartment(self,name,estb_year,deptID):
        self.dept = Department(name,estb_year,deptID)
    def GetEmployeeID(self,userName, password):
        self.name=userName
        self.password=password
        self.EmpID = user.Login(self)
        return 
    def setDate(self,ssalary_date,esalary_date):
        self.start_salary_date=ssalary_date
        self.end_salary_date = esalary_date
        return
    def setBankInfo(self,Bankinfo):
        self.bank_info=Bankinfo
    def __str__(self):
        return str(self.EmpID)+"\t"+str(self.dept)+"\t"+self.start_salary_date+"\t"+self.end_salary_date+"\t"+str(self.bank_info)+"\t"+str(self.basic_salary)+"\t"+str(self.housing_allowance)+"\t"+str(self.children_allowance)+"\t"+str(self.social_allowance)+"\t"+str(self.transportation_allowance)+ "\t"+str(self.Emirati_pension)+"\t"+str(self.car_loan)+"\t"+str(self.house_loan)
class Manager(Employee):
    def __init__(self,basic_salary=100,housing_allowance=0, children_allowance=0, social_allowance=0,
                 transportation_allowance=0, Emirati_pension=0.05, car_loan=0, house_loan=0):
        Employee.__init(self,basic_salary,housing_allowance, children_allowance, social_allowance,
                 transportation_allowance, Emirati_pension, car_loan, house_loan)
        self.EmployeList=[]                     # To keep managed only 25 employees
                                               # 7% additional allowance
        self.housing_allowance=self.housing_allowance*1.7
        self.children_allowance=self.children_allowance*1.7 
        self.social_allowance=self.social_allowance*1.7
        self.transportation_allowance=self.transportation_allowanc*1.7 
    def CalculatePay(self):
        Employee.CalculateNetPay(self)
    def AddEmployeeToList(self, emp):
        try:
            if len(Employee)==25:
                raise
            else:
                self.Employelist.append(emp)
        except:
            print("Can not assign more than 25 employee to manager")
            
    def setDept(self,name,estb_year,deptID):
        self.setDepartment(name,estb_year,deptID)
    def getEmp_Info(self,userName, password):
        self.GetEmployeeID(userName,password)
    def setSalaryDate(self,stDate,edDate):
        self.setDate(stDate,edDate)
    def set_Bank_Info(self,bank_name,branch_name,account_number):
        self.setBankInfo(BankInfo(bank_name,branch_name,account_number))    
class Manager(Employee):
    def __init__(self):
        Employee.__init(self)
        self.EmployeList=[]                     # To keep managed only 25 employees
                                               # 7% additional allowance
        self.housing_allowance=self.housing_allowance*1.7
        self.children_allowance=self.children_allowance*1.7 
        self.social_allowance=self.social_allowance*1.7
        self.transportation_allowance=self.transportation_allowanc*1.7 
    def CalculatePay(self):
        Employee.CalculateNetPay(self)
    def AddEmployee(self, emp):
        try:
            if len(Employee)==25:
                raise
            else:
                self.file_mang.AddEmployee(self)
        except:
            print("Can not assign more than 25 employee to manager")
            
    def setDept(self,name,estb_year,deptID):
        self.setDepartment(name,estb_year,deptID)
    def getEmp_Info(self,userName, password):
        self.GetEmployeeID(userName,password)
    def setSalaryDate(self,stDate,edDate):
        self.setDate(stDate,edDate)
    def set_Bank_Info(self,bank_name,branch_name,account_number):
        self.setBankInfo(BankInfo(bank_name,branch_name,account_number))   
class HR(user):
    def __init__(self,name,password):
        user.__init__(self,name,password)
        self.EmployeeFile=""
        self. fileMan = FileManager()
    def Login(self):
        return user.Login(self)
    def printEmployee(self,EmpID):
        userInfo,emp = self.fileMan.getUserInfo(EmpID)
        print("PERSONAL INFORMATION ")
        print("----------------------------")
        print("Employee Name : "+userInfo[1]+"\t\t\t\t\t\t"+"Bank Name : "+emp[4])
        print("Employee ID   : "+emp[0]+"\t\t\t\t\t\t"+"Branch Name :"+emp[5])
        print("Department   : "+emp[1].split('__')[0]+"\t\t\t\t\t"+"Account No :"+emp[6])        
    def printSalaryDetail(self,sdate,edate,EmpID):
        lst = self.fileMan.GetSEDateSalary(sdate,edate,EmpID)
        print("\n\n")
        print("PAY ROLL INFORMATION")
        print("-------------------------")
        print("Start Date : "+sdate)
        print("End   Date : "+edate)
        basic_salary=0.0
        housing_allowance=0.0
        children_allowance=0.0
        social_allowance=0.0
        transportation_allowance=0.0
        Emirati_pension=0.0
        car_loan=0.0
        house_loan=0.0
        for i in lst:
            basic_salary+=float(i[7])
            housing_allowance+=float(i[8])*float(i[7])
            children_allowance+=float(i[9])*float(i[7])
            social_allowance+=float(i[10])*float(i[7])
            transportation_allowance+=float(i[11])*float(i[7])
            Emirati_pension+=float(i[12])*float(i[7])
            car_loan+=float(i[13])*float(i[7])
            house_loan+=float(i[14])*float(i[7])
        total_earning = basic_salary + (housing_allowance +children_allowance+social_allowance+transportation_allowance)*basic_salary
        deduction = (Emirati_pension+car_loan+house_loan)*basic_salary
        net = total_earning+deduction
        print("SUMMARY OF PAYMENT ")
        print("Total Earnings\t \t| \tTotal Deductions \t | \tNet Pay (Total Salary)")
        print(str(total_earning)+"\t|\t"+str(deduction)+"\t|\t"+str(net))
        print("-------------------------------------------------------------------------------------------------------------")
        print("EARNING \t \t \t \t \t \t \t DEDUCTION")
        print("-------------------------------------------------------------------------------------------------------------")
        print("Description\t|\t Amount \t\t\t\t Description\t\t|\t\t Amount ")
        print("Basic Salary \t\t : "+str(basic_salary)+"\t\t\t\t Car loan \t : "+str(car_loan))
        print("Housing Allowance \t : "+str(housing_allowance)+"\t\t\t House loan \t : "+str(house_loan))
        print("Social Allowance \t : "+str(social_allowance)+"\t\t\t Emitati Pension : "+str(Emirati_pension))
        print("Children Allowance \t : "+str(children_allowance)+"\t\t\t Total \t\t : "+str(car_loan+house_loan+Emirati_pension))
        print("Transportation Allowance : "+str(transportation_allowance))
        print("Total      \t\t : "+str(children_allowance+social_allowance+housing_allowance+transportation_allowance))
        
        
#         Children Allowance
#         Transportation Allowance
#         Total
    def printAllEmployee(self):
        All_data = self.fileMan.getAllUserInfo()
#         '10000', 'Johna', 'Pakistan', 'abc@gmail.com', 'Islamabad Paksitan', '+92332343434'
        print("ID\tUserName\tPassword\tE-mail\t\tAddress\t\t\tPhone Number")
        print("----------------------------------------------------------------------------------------------")
        for record in All_data:
            if record=='':
                continue
            spltData = record.split('\t')
            print(spltData[0]+"\t"+spltData[1]+"\t\t"+spltData[2]+"\t"+spltData[3]+"\t"+spltData[4]+"\t"+spltData[5])
    def AddEmployee(self,userInfo,Emp):
        self.fileMan.AddEmployee(Emp)
        print("Successfully added")
    def RemoveEmployee(self, EmpID):
        self.fileMan.RemoveEmployee(EmpID)
# Validaiton function for input

def Validation(mesg):
    while True:
        try:
            val= float(input(mesg))
            return val
        except : 
            print("Please "+mesg.replace(":","")+" in numbers")
def DateValidation(mesg):
    dat = input(mesg)
    while True:
        val = dat.split("-")
        try:
            int(val[0])
            int(val[2])
            if len(val[1]!=3):
                print("Enter your month")
            else:
                return dat
        except:
            print("Enter valid format ")
            dat = input(mesg)
# Menu for user interaction 
def Menu():
    print("**** WELCOME TO SPACK INFOTECH PAYROLL SYSTEM****")
    print("Press 1 for adding new employee")
    print("Press 2 for viewling all employees")
    print("Press 3 for viewing salary of specific employee between dates")
    print("Press 4 for removing employee ")
    print("Press 0 for exit ")
    while True:
        try:
            inpt = int(input("Enter your choise"))
            if inpt>=0 and inpt<=4:
                return inpt
            else:
                print("Enter valind input")
        except: 
            print("Enter valid input")
# Dummy user generation
# To Add data into userfile through classes


EmployeeCrendential=[]
for i  in (['a','i','o','u','e']):
    f = user("John"+i,"Pakistan","Islamabad Paksitan","abc@gmail.com","+92332343434")
    f.RegisterUser()
    f=user("Eliva"+i,"Pakistan","Islamabad Paksitan","abc@gmail.com","+92332343434")
    f.RegisterUser()
    f=user("Atif"+i,"Pakistan","Islamabad Paksitan","abc@gmail.com","+92332343434")
    f.RegisterUser()
    f =user("Asalm"+i,"Pakistan","Islamabad Paksitan","abc@gmail.com","+92332343434")
    f.RegisterUser()
    f=user("Jude"+i,"Pakistan","Islamabad Paksitan","abc@gmail.com","+92332343434")
    f.RegisterUser()    
    EmployeeCrendential.append(("John"+i,"Pakistan"))
    EmployeeCrendential.append(("Eliva"+i,"Pakistan"))
    EmployeeCrendential.append(("Atif"+i,"Pakistan"))
    EmployeeCrendential.append(("Asalm"+i,"Pakistan"))
    EmployeeCrendential.append(("Jude"+i,"Pakistan"))
department = ["IT","Testing","Art & Design"]
deptID = ["101","203","405"]
estb_year = ["1990","2001","2004"]
FileMan = FileManager()
for mon in ["NOV","DEC"]:
    for Emp_record in EmployeeCrendential:
        basic_salary=100000.0       # suppose basic salary is fix, 
                                # For manager, it will automatically be calcualted 
        # Assume we are assigning random % to allowance and loan betweem 0 and 10%
        housing_allowance=random.uniform(0, 0.1)
        children_allowance=random.uniform(0, 0.1)
        social_allowance=random.uniform(0, 0.1)
        transportation_allowance=random.uniform(0, 0.1)
        Emirati_pension=random.uniform(0, 0.1)
        car_loan=random.uniform(0, 0.1)
        house_loan=random.uniform(0, 0.1)
        Emp = Employee(basic_salary,housing_allowance, children_allowance, social_allowance,
                       transportation_allowance, Emirati_pension, car_loan, house_loan)
        dept_indx=random.randint(0,2)  # Randomly assigning departments
        Emp.setDepartment(department[dept_indx],estb_year[dept_indx],deptID[dept_indx])
  
        Emp.GetEmployeeID(Emp_record[0],Emp_record[1])
        bnkInfo=BankInfo("HBL","HBL Lahore","AC0"+str(random.randint(0,9))+"0101020304"+str(random.randint(0,9)))
        Emp.setBankInfo(bnkInfo)
        Emp.setDate("01-"+mon+"-2018","30-"+mon+"-2018")
        FileMan.AddEmployee(Emp)
f = user("HR","HR201921","Washngton, USA","HR2019@gmail.com","+842332343434")
f.RegisterUser()
print("**** WELCOME TO SPACK INFOTECH PAYROLL SYSTEM****")

######### Here User Input 
#        ## HR Login validation 

while True:
    HRUserName = input("Enter HR user Name")
    HRPassword = input("Enter HR Password")
    hR = HR(HRUserName,HRPassword)
    if hR.Login()==-1:
        print("Plese try again")
    elif hR.Login()!=10050:
        print("Plese Enter HR detail")
    else:
        print("Successful login")
        break;

hR = HR("HR","HR201921")
chck = Menu()
while True:
    if chck==1:
        # # Add new employee data detail, input from user 
        name = input("Enter Employee Name : ")
        password = input("Enter password : ")
        address = input("Enter Password : ")
        email = input("Enter email address : ")
        mob = input("Enter mobile number in format i.e +9233432453432")
        usr = user(name,password,address,email,mob)
        usr.RegisterUser()
        while True:
                # allowance, basic pay and loan detail input 
                basic_salary= Validation(" enter your basic salary : ") 
                housing_allowance=Validation(" enter house allownce in between 0 to 1")
                children_allowance=Validation(" enter children allownce in between 0 to 1")
                social_allowance=Validation(" enter social allownce in between 0 to 1")
                transportation_allowance=Validation(" enter trasnport allownce in between 0 to 1")
                Emirati_pension=Validation(" enter Emirati_pension in between 0 to 1")
                car_loan=Validation(" enter car loan in between 0 to 1")
                house_loan=Validation(" enter house loan in between 0 to 1")
                emp = Employee(basic_salary,housing_allowance, children_allowance, social_allowance,transportation_allowance, Emirati_pension, car_loan, house_loan)
                # department input 
                deptName = input("Enter department Name ")
                estb_year = input("Enter established year ")
                deptID = input("Enter departmetn ID ")
                emp.setDepartment(deptName,estb_year,deptID)
                emp.GetEmployeeID(name,password)

                # start date and end date input 
                sdate= DateValidation("Enter Start date, i.e 01-NOV-2018")
                edate= DateValidation("Enter End date, i.e 30-NOV-2018")
                emp.setDate(sdate,edate)

                # Bank detail input 
                bank_name= input("Enter bank Name ")
                branch_name = input("Enter bank branch ")
                account_number = input("Enter account number")
                bnk = BankInfo(bank_name,branch_name,account_number)
                emp.setBankInfo(bnk)
                hR.AddEmployee(usr,emp)
                break
    elif chck==2:
        hR.printAllEmployee()
    elif chck==3:
        empID =Validation(" Enter Employee ID 5 digits ") 
        sdate= DateValidation("Enter Start date, i.e 01-NOV-2018")
        edate= DateValidation("Enter End date, i.e 30-NOV-2018")
        hR.printEmployee(empID)
        hR.printSalaryDetail(sdate,edate,empID)  
    elif chck==4:
        empID =Validation(" Enter Employee ID 5 digits ") 
        RemoveEmployee(empID)
    else:
        break
