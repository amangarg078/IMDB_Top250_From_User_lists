import requests
import lxml
from lxml import html
import time
import sqlite3
import re
import psycopg2



def getMovies():
    conn=psycopg2.connect("dbname='imdb' user='postgres' password='postgres'")
    cursor=conn.cursor()
    top250=requests.get('http://www.imdb.com/chart/top?ref_=nv_mv_250_6')
    tree_250=html.fromstring(top250.content)
    mov_links=tree_250.xpath('//tbody[@class="lister-list"]/tr/td[@class="titleColumn"]/a/@href')
    movie_titles=tree_250.xpath('//tbody[@class="lister-list"]/tr/td[@class="titleColumn"]/a/text()')
    
    
    movie=[]
    movies_dict={}
    user_list=[]
    #loop will run for all movies in top 250 list. 
    for i in range(len(mov_links)):
        movie_link="http://www.imdb.com"+mov_links[i]
        m=re.match(r'.*(tt[0-9]+)',movie_link)
        movie_title=movie_titles[i]
        movie_id=m.group(1)
        movie.append(movie_id)
        time.sleep(5)
        try:
            movie_page=requests.get(movie_link)
        
            movie_page_tree=html.fromstring(movie_page.content)
        except:
            print "Request failed for ",movie_link
            pass
                
            
        movie_count=1
        try:
            movie_year=movie_page_tree.xpath('//*[@id="titleYear"]/a/text()')[0]
        except:
            movie_year=""
            pass
        try:
            movie_rating=movie_page_tree.xpath('//div[@class="ratingValue"]/strong/span/text()')[0]
        except:
            movie_rating=""
            pass
        try:
            
            movie_rating_count=movie_page_tree.xpath('//div[@class="imdbRating"]/a/span[@itemprop="ratingCount"]/text()')[0]
        except:
            movie_rating_count=0
            pass
        try:
            movie_image=movie_page_tree.xpath('//div[@class="poster"]/a/img/@src')[0]
            
        except:
            movie_image="#"
            pass
        try:
            movie_summary=' '.join(movie_page_tree.xpath('//div[@class="summary_text"]/text()')[0].split())
        except:
            movie_summary=""
            pass
        try:
            movie_user_list_all_link="http://www.imdb.com"+movie_page_tree.xpath('//*[@id="relatedListsWidget"]/div[7]/a/@href')[0]
        except:
            movie_user_list_all_link=""
            pass
        
        movies_dict[movie_title]=[movie_rating,int(''.join(movie_rating_count.split(','))),movie_year,movie_image,movie_summary,unicode(movie_link),movie_count,movie_id]
        cursor.execute('insert into "IMDBMostPopular_movie"\
            (movie_title,movie_rating,movie_rating_count,movie_year,movie_image,movie_summary,movie_link,movie_count)\
            values( %s,%s,%s,%s,%s,%s,%s,%s)', (movie_title,movies_dict[movie_title][0],movies_dict[movie_title][1],movies_dict[movie_title][2],movies_dict[movie_title][3],movies_dict[movie_title][4],movies_dict[movie_title][5],movies_dict[movie_title][6]))
        conn.commit()

        time.sleep(1)
        try:
            all_list_page=requests.get(movie_user_list_all_link)
        except:
            print "Request not made for ",movie_user_list_all_link
            pass
        movies_dict,movie,cursor,conn=UserList(all_list_page,movies_dict,movie,user_list,cursor,conn)
    cursor.close()
    conn.close()
    #movies_dict has all the info on the field. Can be used anywhere.
    return movies_dict

def UserList(all_list_page,movies_dict,movie,user_list,cursor,conn):
    user_list_tree=html.fromstring(all_list_page.content)
    user_list_links_list=user_list_tree.xpath('//div[@class="list-preview-item-wide"]/a/@href')
    #looping over all the user lists.
   
    for j in range(len(user_list_links_list)):
        movie_user_list_link="http://www.imdb.com"+user_list_links_list[j]
        if movie_user_list_link not in user_list:
            user_list.append(movie_user_list_link)
            time.sleep(2)
            try:
                movie_user_list_page=requests.get(movie_user_list_link)
            except:
                print "Request not made for ",movie_user_list_link
                pass
            movies_dict,movie,cursor,conn=moviesFromUserList(movie_user_list_page,movies_dict,movie,user_list,cursor,conn)
            
    return movies_dict,movie,cursor,conn



def moviesFromUserList(movie_user_list_page,movies_dict,movie,user_list,cursor,conn):
    movie_user_list_page_tree=html.fromstring(movie_user_list_page.content)
    movie_list_from_user_list=movie_user_list_page_tree.xpath('//div[@class="list detail"]/div/div/b/a/@href')
    movie_name_list=movie_user_list_page_tree.xpath('//div[@class="list detail"]/div/div/b/a/text()')
    #looping over all movies in the user list
    for k in range(len(movie_list_from_user_list)):
        mov_link_from_user_list="http://www.imdb.com"+movie_list_from_user_list[k]
        m=re.match(r'.*(tt[0-9]+)',mov_link_from_user_list)
        movie_id=m.group(1)
        time.sleep(5)
        if movie_id not in movie:
            
            movie_title=movie_name_list[k]
            
            movie.append(movie_id)
            
            movie_count=1
            try:
                movie_page=requests.get(mov_link_from_user_list)
                movie_page_tree=html.fromstring(movie_page.content)
            except:
                print "Request could not be completed for",mov_link_from_user_list
                pass
            try:
                movie_year=movie_page_tree.xpath('//*[@id="titleYear"]/a/text()')[0]
            except:
                movie_year=""
                pass
            try:
                movie_rating=movie_page_tree.xpath('//div[@class="ratingValue"]/strong/span/text()')[0]
            except:
                movie_rating=""
                pass
            try:
                movie_rating_count=movie_page_tree.xpath('//div[@class="imdbRating"]/a/span[@itemprop="ratingCount"]/text()')[0]
            except:
                movie_rating_count=0
                pass
            try:
                movie_image=movie_page_tree.xpath('//div[@class="poster"]/a/img/@src')[0]
            except:
                movie_image="#"
                pass
            try:
                movie_summary=' '.join(movie_page_tree.xpath('//div[@class="summary_text"]/text()')[0].split())
            except:
                movie_summary=""
                pass
             
            movies_dict[movie_title]=[movie_rating,int(''.join(movie_rating_count.split(','))),movie_year,movie_image,movie_summary,unicode(mov_link_from_user_list),movie_count,movie_id]
            cursor.execute('insert into "IMDBMostPopular_movie"\
                (movie_title,movie_rating,movie_rating_count,movie_year,movie_image,movie_summary,movie_link,movie_count)\
                values( %s,%s,%s,%s,%s,%s,%s,%s)', (movie_title,movies_dict[movie_title][0],movies_dict[movie_title][1],movies_dict[movie_title][2],movies_dict[movie_title][3],movies_dict[movie_title][4],movies_dict[movie_title][5],movies_dict[movie_title][6]))
            conn.commit()                
                  
        else:
            
                    
            for key in movies_dict:
                if movie_id in movies_dict[key][7]:
                    movies_dict[key][6]+=1
                    cursor.execute('update "IMDBMostPopular_movie" set movie_count=movie_count+1 where movie_title=%s',(key,))
                    conn.commit()       
    return movies_dict,movie,cursor,conn





          
        

