import logging

from flask import Flask, json, session, render_template
from flask_ask import Ask, request, session, question, statement, context

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

openstream = open("AttendenceSheet.txt","r")
content = openstream.read().splitlines()
openstream.close();

openstream = open("Grades.txt","r")
gradescontent = openstream.read().splitlines()
openstream.close();


gradestring =""
for i in range(len(gradescontent)):
    gradestring = gradestring +"............................................................................" + gradescontent[i]

openstream = open("Announcements.txt","r")
announcementscontent = openstream.read().splitlines()
openstream.close();

announcstring =""
for i in range(len(announcementscontent)):
    announcstring = announcstring +"............................................................................" + announcementscontent[i]

@ask.launch
def lauchfunc():
    welcome_msg = render_template('welcome')
    session.attributes["counter"] = str(0)
    session.attributes["counter2"] = str(0)
    return question(welcome_msg)

@ask.intent("AttendanceIntent")
def attendancefunc():
    if len(content)> int(session.attributes.get("counter")):
        counterint= session.attributes.get("counter")
        session.attributes["counter"] = str(int(counterint)+1)
        return question(content[int(counterint)]) 
    else:
        session.attributes["counter"] = str(0)
        return question("The list is finished....Do you want to end the application or choose another option").standard_card("Attendance Status","Attendance has been taken for the class successfully");

@ask.intent("PresentIntent")
def presentfunc():
    counterint= session.attributes.get("counter")
    counterint=int(counterint)-1
    openstream = open("AttendenceResult.txt", "r");
    old = openstream.read();
    openstream.close();
    writestream = open("AttendenceResult.txt","w")
    if counterint==0:
        writestream.write("")
    elif counterint!=0:
        writestream.write(old);
        writestream.write("\n")
    writestream.write(content[counterint] + "   "+ "Present")
    writestream.close()
    return question("Recorded")
      
@ask.intent("AbsentIntent")
def absentfunc():
    counterint= session.attributes.get("counter")
    counterint=int(counterint)-1
    openstream = open("AttendenceResult.txt", "r");
    old = openstream.read();
    openstream.close();
    writestream = open("AttendenceResult.txt","w")
    if counterint==0:
        writestream.write("")
    elif counterint!=0:
        writestream.write(old);
        writestream.write("\n")
    writestream.write(content[counterint] + "   "+ "Absent")
    writestream.close()
    return question("Recorded")


@ask.intent("GradesIntent")
def gradesfun():
    session.attributes["counter"] = str(0)
    openstream = open("Grades.txt","r")
    gradescontent = openstream.read().splitlines()
    openstream.close();
    gradestring =""
    for i in range(len(gradescontent)):
        gradestring = gradestring +"............................................................................" + gradescontent[i]
    strinx="Do you want to end the application or choose another option";
    return question(gradestring+"............................................................"+strinx).standard_card("Grade Status","Grades have been announced to the class today");

@ask.intent("AnnouncementsIntet")
def announcefunc():
    session.attributes["counter"] = str(0)
    strinx="Do you want to end the application or choose another option";
    return question(announcstring+"............................................................"+strinx).standard_card("Class Plan", "The class plan has been covered today");

@ask.intent("RecordingGradesIntent")
def recordingfunc():
   if len(content)> int(session.attributes.get("counter2")):
        counterint= session.attributes.get("counter2")
        session.attributes["counter2"] = str(int(counterint)+1)
        return question(content[int(counterint)]+"'s grade") 
   else:
        session.attributes["counter2"] = str(0)
        return question("The list is finished....Do you want to end the application or choose another option").standard_card("Grades Recorded","Grades have been successfully recorded");
    
@ask.intent("NumberIntent", mapping={'Numberinput':'Number'})
def numberfunc(Numberinput):
    counterint= session.attributes.get("counter2")
    counterint=int(counterint)-1
    openstream = open("Grades.txt", "r");
    old = openstream.read();
    openstream.close();
    writestream = open("Grades.txt","w")
    if counterint==0:
        writestream.write("")
    elif counterint!=0:
        writestream.write(old);
        writestream.write("\n")
    writestream.write(content[counterint] + "   "+ str(Numberinput))
    writestream.close()
    return question("Recorded")

@ask.intent("OptionsIntent")
def optiofunc():
    return question("Choose one of the following options: Attendance"+"............................................................................" +"or Recording Grades"+"............................................................................"+" or Announcing Grades or" +"............................................................................"+" Telling the Announcements")

@ask.intent("StopIntent")
def session_ended():
    return statement("Thank you for using class assist, hope you enjoyed the application")

if __name__ == '__main__':
    app.run(debug=True)