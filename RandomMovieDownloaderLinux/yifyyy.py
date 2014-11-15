# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox

import urllib
import json
import webbrowser
import random

import sys
from string import digits


top = Tk()
top.geometry("700x700+30+30")
top.title('Movie Downloader')
top['bg']="#D3D8E8"


def download(link,name):
    reply=tkMessageBox.askokcancel(title='Movie',message='Name of the movie is '+name+'. Do you want to continue?')
    if (reply==True):
        
        if link:
            #movieurl=movieurl[1:]
            webbrowser.open_new_tab(link)    
    
def watch(url):
    webbrowser.open_new_tab(url)

def moviedetails():
    uquality=quality.get()
    urating=rating.get()
    urating=urating[0]
    ugenre=genre.get()
    uname=name.get()
    if uquality=="Quality":
        uquality="720p"
    if urating=="Rating":
        urating="1+"
    if ugenre=="Genre":
        ugenre="All"
    if uname:
        rating.set('Rating')
        genre.set('Genre')
        url = "https://yts.re/api/list.json?limit=1&quality="+uquality+"&keywords="+uname
    else:
        url="https://yts.re/api/list.json?limit=50&quality="+uquality+"&rating="+urating+"&genre="+ugenre
    print url
    try:
        response = urllib.urlopen(url).read()
        jsonvalues = json.loads(response)
    except IOError:
                tkMessageBox.showerror(title='Not Availabel',message='Internet Connection needs to be checked')
    if 'MovieList' in jsonvalues.keys():
        movielist=jsonvalues['MovieList']
        no_movies=len(movielist)
        if no_movies!=0:
            if no_movies!=1:
                i=random.randrange(0,no_movies)
            else:
                i=0
            #for i in range(0,len(movielist)):
            torrentdetails=movielist[i]
            movieid=torrentdetails['MovieID']
            idurl="https://yts.re/api/movie.json?id="+movieid
            #print idurl
            try :
                responseforid=urllib.urlopen(idurl).read()
                moviedetails=json.loads(responseforid)
            except IOError:
                tkMessageBox.showerror(title='Not Availabel',message='Internet Connection needs to be checked')
                
            flag=1
            tempuname=uname.strip("0123456789")
            if uname:
                if (moviedetails['MovieTitle'].lower()).find(tempuname.lower())!=-1:
                    flag=0
                    print "yes"
                else:
                    print "not"
            if not uname:
                flag=0
            if flag==0:
                
                nameofmovie=StringVar()
                nameofmovie.set('Title: '+moviedetails['MovieTitle'])
                
                    
                label = Label( top, textvariable=nameofmovie,fg='#0e385f',bg='#D3D8E8')
                label.place(x=50,y=220,width=500,height=30)

                movierating=StringVar()
                movierating.set('ImdbRating : '+moviedetails['MovieRating'])
                label = Label( top, textvariable=movierating,fg='#0e385f',bg='#D3D8E8')
                label.place(x=50,y=260,width=300,height=30)
                
                movieruntime=StringVar()
                movieruntime.set('MovieRuntime : '+moviedetails['MovieRuntime'])
                label = Label( top, textvariable=movieruntime,fg='#0e385f',bg='#D3D8E8')
                label.place(x=50,y=300,width=300,height=30)
                
                youtube=StringVar()
                youtube.set('Click to watch Trailer : ')
                label = Label( top, textvariable=youtube,fg='#0e385f',bg='#D3D8E8')
                label.place(x=50,y=340,width=300,height=30)

                youtubelink=moviedetails['YoutubeTrailerUrl']
                link = Button(top, text ="Watch", command = lambda:watch(youtubelink),bg='#3b5998',fg='white')
                link.place(x=360,y=340 ,width=100 ,height=30)
                #top.mainloop()

                shortdescp=moviedetails['ShortDescription']
                sdesc=StringVar()
                sdesc.set('Short Description :')
                label = Label( top, textvariable=sdesc,fg='#0e385f',bg='#D3D8E8')
                label.place(x=50,y=375,width=300,height=30)

                lengthofshort=len(shortdescp)
                no=lengthofshort/75
                temp2=0
                temp3=0
                for j in range(0,no+1) :
                    shortdesc=StringVar()
                    
                    temp=shortdescp.find(' ',(75*j)+75,(75*j)+90)
                    temp2=temp
                    temp=temp%75
                    stri=shortdescp[(75*j)+temp3:(75*j)+75+temp]
                    temp3=temp2%75
                    shortdesc.set(stri)
                    label = Label( top, textvariable=shortdesc,fg='#0e385f',bg='#D3D8E8')
                    if j!=no:
                        label.place(x=50,y=(400+(30*j)),width=600,height=30)
                    else:
                        t=j%4
                        label.place(x=50,y=(400+(30*j)),width=600,height=30)
                        label = Label( top, text='',fg='#0e385f',bg='#D3D8E8')
                        label.place(x=50,y=(400+(30*(j+1))),width=600,height=30*t)
                
                current=400+(4*30)
                castlist=moviedetails['CastList']
                actors=""
                for i in range(0,len(castlist)):
                    if i==(len(castlist)-2):
                        actors=actors+castlist[i]['ActorName']+" and "
                    elif i==(len(castlist)-1):
                        actors=actors+castlist[i]['ActorName']
                    else :
                        actors=actors+castlist[i]['ActorName']+', '
                        
                act=StringVar()
                act.set('Cast : '+actors)
                label = Label( top, textvariable=act,fg='#0e385f',bg='#D3D8E8')
                label.place(x=50,y=current+30,width=500,height=30)
                
             
                
                maglink=moviedetails['TorrentMagnetUrl']
                namemov=moviedetails['MovieTitle']
                link = Button(top, text ="Download", command = lambda:download(maglink,namemov),bg='#3b5998',fg='white')
                link.place(x=360,y=current+60 ,width=100 ,height=30)
                   
                #print moviedetails
                """prin0t nameofmovie"""
            else:
                tkMessageBox.showerror(title='Not Available',message='Torrent File not available on YIFY')
        else:
            tkMessageBox.showerror(title='Not Available',message='Torrent File not available on YIFY')
    else:
        tkMessageBox.showerror(title='Not Available',message='Torrent File not available on YIFY')
    
    
B = Button(top, text ="MovieDetails", command = moviedetails,bg='#3b5998',fg='white')

label = Label( top, text="Enter name of the movie*",fg='#0e385f',bg='#D3D8E8',font=("Helvetica", 12))
label.place(x=20,y=60,width=200,height=30)
moviename = StringVar()
name = Entry(top, textvariable=moviename)
name.config(font=('Helvetica',(10)),bg='white',fg='black')

name.place(x=240,y=60,width=300,height=30)
label = Label( top, text="Random Movie Downloader ",fg='#0e385f',bg='#D3D8E8',font=("Helvetica", 10))
label.place(x=20,y=120,width=200,height=30)
rating=StringVar()
rating.set('Rating')
choices = ['4+', '5+', '6+', '7+','8+', '9+']
option = OptionMenu(top, rating, *choices)
option.config(font=('Helvetica',(10)),bg='#3b5998',fg='white')
option.place( x=300,y=120,width=80,height=30)
quality=StringVar()
quality.set('Quality')
qualitychoices = ['720p', '1080p', '3d']
option = OptionMenu(top, quality, *qualitychoices)
option.config(font=('Helvetica',(10)),bg='#3b5998',fg='white')
option.place( x=210,y=120,width=80,height=30)
genre=StringVar()
genre.set('Genre')
genrechoices = ['All', 'Action', 'Animation', 'Comedy','Documentary', 'Family','Film-Noir','Horror','Musical','Romance','Sport','War','Adventure','Biography','Crime','Drama','Fantasy','History','Music','Mystery','Sci-Fi','Thriller','Western']
option = OptionMenu(top, genre, *genrechoices)
option.config(font=('Helvetica',(10)),bg='#3b5998',fg='white')
option.place( x=410,y=120,width=200,height=30)
label = Label( top, text="*name field can be left empty for random download",fg='#0e385f',bg='#D3D8E8',font=("Helvetica", 10))
label.place(x=200,y=610,width=300,height=30)

label = Label( top, text="©Melvin Philips Y.N.W.A",fg='#0e385f',bg='#D3D8E8',font=("Helvetica", 10))
label.place(x=400,y=640,width=200,height=30)



B.place(x=280,y=180,width=100,height=30)
top.mainloop()

