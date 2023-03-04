import multiprocessing as mp
import itertools

def execute_extraction(self, params):
    jsondict = {}
    limit = 4
    flag = True
    while flag:
        for page in itertools.count(start=1, step=limit):
            queries = self.source_extract_gql(params, page, limit)
            print('queries')
            print(queries)
            pool = mp.Pool(4)
            try:
                all_res = pool.map(self.raise_request, queries)            
                # all_res (List of Dictionaries) --> [{'incident':[{'id':'abc'}]}, {} ]
                for i in range(len(all_res)):
                    objstr = [k for k, v in all_res[i].items()][0]
                    if objstr not in jsondict and len(all_res[i][objstr]) > 0:
                        jsondict[objstr] = all_res[i][objstr]
                    elif objstr in jsondict and len(all_res[i][objstr]) > 0:
                        size_per_page = len(all_res[i][objstr])
                        for pg in range(size_per_page):
                            jsondict[objstr].append(all_res[i][objstr][pg])
                    elif objstr in jsondict and len(all_res[i][objstr]) < 1:
                        flag = False
                        break
            except:
                pool.terminate()
                break
            else:
                print('normal')
        limit += 4
        pool.close()
        pool.join()
        if not flag:
            break
    return jsondict
            