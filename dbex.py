if __name__ == '__main__':
   table_name = 'Pages2'
#   create_table(table_name)
   item = {}
   item['url']='url1'
   item['word']='word1'
   item['word_count']=15
   item['hyperlinks']=['hard','to','combine']
   add_item(item,table_name)

   item2 = {}
   item2['url']='hard'
   item2['word']='word1'
   item2['word_count']=16
   item2['hyperlinks']=['blabla','to','combine']
   add_item(item2,table_name)

   response1 = get_word_count_in_page('word1','url1', table_name)
   response2 = get_word_count_in_page('not_in_table','url1', table_name)

   print(response1)
   print(response2)

   response3 = get_top_urls_for_word('word1',2,table_name)
   print(response3)
   print('number of results ',response3['Count'])
   print('first count', response3['Items'][0]['word_count'])
   print('second count', response3['Items'][1]['word_count'])