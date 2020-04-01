from github import Github
import time
import datetime
import json

global dict_rep
global remaining_limit 
global next_request_time 

g = Github("apyspo", "51github51")
# query='language:python'
#repositories = g.search_repositories("github", sort="stars", order="desc", language="Python")
library_set = set([])

dict_rep = {}
#6. sayfaya kadar most starred repositories
with open('dict_repositories.json') as file:
    dict_rep_file=json.load(file) # use `json.loads` to do the reverse

#dict_rep = { "repository_name" : "scikit-learn/scikit-learn" }
dict_rep=dict_rep_file.popitem()[1]
#dict_rep = dict_rep_file

remaining_limit = g.get_rate_limit()
next_request_time = datetime.datetime.fromtimestamp(g.rate_limiting_resettime)

#with open('dict_rep_libs' + str(next_request_time) + '.json') as file:
#    dict_rep_libs=json.loads(file) # use `json.loads` to do the reverse

print("wait seconds: " + str((next_request_time - datetime.datetime.now()).seconds))
if (remaining_limit.core.remaining == 0):
    time.sleep((next_request_time - datetime.datetime.now()).seconds)
try:
    while ((datetime.datetime.now() > next_request_time) or (remaining_limit.core.remaining > 0)):
        print("reamining limit: " + str(remaining_limit.core.remaining))
        print(next_request_time)

        repository_item = dict_rep.pop()
        repository_name = repository_item.get("repository_name")
        repository_isprocessed = repository_item.get("processed")

        if repository_isprocessed == "True":
            continue

        if remaining_limit.core.remaining > 0:
            repo = g.get_repo(repository_name)
            #get_collaborators() requires push access to view collaborators.
            #so check if they are in contirbutors list as well

            contributors = repo.get_contributors()
            list_contributors = []
            for contributor in contributors:
                list_contributors.append(contributor.login)

            topics = repo.get_topics() 
            #print(repo.stargazers_count)
            #print("SUBS") cok uzun liste
            #for subs in repo.get_subscribers():

            contents = repo.get_contents("")

            library_set = set([])
            # recursively check all folders in repository
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir" and file_content.name != "venv":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    # check if file .py file
                    if (file_content.name.split(".")[-1] == "py") and (file_content.size < 1024 * 1024):
                        cntLib = 0
                        # decode from bytestring to utf-8
                        for line in file_content.decoded_content.decode("utf-8", errors="ignore").splitlines():
                            #improve with (last import/from line you have seen,if you start not seeing from and import lines for 5 cons lines, skip that file.)
                            if len(line) == 0:
                                continue
                            elif (line[0] == "#" or line[0] == "'" or line[0] == " "):
                                continue
                            if line.split(" ")[0] == "from" or line.split(" ")[0] == "import":
                                if line.split(" ")[1][0] != "." and line.split(" ")[1][0] != "_":
                                    library_set.add(line.split(" ")[1])
                                    #print(line)
                            else:
                                cntLib+=1
                            if cntLib > 5:
                                break
                            else:
                                continue
                        #print(file_content.decoded_content.decode("utf-8", errors="ignore").splitlines())
            dict_rep_json = {}

            with open('dict_rep_libs.json', 'a') as file:
                file.write(',')
                dict_rep_json = { "repository" : repository_name  , "subsriber_count" : repo.get_subscribers().totalCount }
                new_contributors = []
                for contributor in list_contributors:
                    new_contributors.append( { "contributor" : contributor } )
                dict_rep_json.update( { "contributors" : new_contributors } )
                new_topics = []
                for topic in topics:
                    new_topics.append( { "topic" : topic } )
                dict_rep_json.update( { "topics" : new_topics } )
                python_libs = []
                for python_lib in list(library_set):
                    python_libs.append( { "python_module" : python_lib } )
                dict_rep_json.update( { "python_modules" : python_libs }) 
                #print(dict_rep_json)
                #dict_rep_json = { "repository" : repository_name, "contributors" : list_contributors, "topics" : topics, "subsriber_count" : repo.get_subscribers().totalCount, "python_modules": list(library_set) }
                file.write(json.dumps(dict_rep_json)) 
                #file.write('\n')
            print(repository_name)
            repository_item.update({"processed": "True"})
            dict_rep.append(repository_item)
        else:
            next_request_time = datetime.datetime.fromtimestamp(g.rate_limiting_resettime)
            #time.sleep(300)
            remaining_limit = g.get_rate_limit()
            time.sleep(next_request_time - datetime.datetime.now())
            if remaining_limit.core.remaining > 0:
                continue
            else:
                time.sleep(300)
                continue

except Exception as e:
    print(e)
    print(repository_name)
    with open('dict_repositories_notprocessed.json', 'w') as file:
        file.write(json.dumps( { "repositories": dict_rep } )) 
    #with open('dict_rep_libs.json', 'a') as file:
        #file.write(json.dumps(dict_rep_libs))
        #file.write('\n')