 
import networkx as nx
import matplotlib.pyplot as plt
import database_handler as db
#draw chart

def draw_chart(word,n):
  table_name = 'PageDetails'
  response = db.get_top_urls_for_word(word, n, 'PageDetails')
  G = nx.Graph()

  G.add_node(word)
  #urls = response(['Items'])
  # print(response)
  for url in response['Items']:
    G.add_node(url['url'])
    G.add_edge(word,url['url'],weight = url['word_count'])

  nx.draw(G,with_labels=True)
  plt.savefig("chart.png")
  plt.show()

if __name__ == '__main__':
  table_name = 'PageDetails'
  db.create_table(table_name)
  item = {}
  item['url'] = 'url1'
  item['word'] = 'word1'
  item['word_count'] = 15
  item['hyperlinks'] = ['hard', 'to', 'combine']
  db.add_item(item, table_name)

  item2 = {}
  item2['url'] = 'hard'
  item2['word'] = 'word1'
  item2['word_count'] = 16
  item2['hyperlinks'] = ['blabla', 'to', 'combine']
  db.add_item(item2, table_name)
  draw_chart("word1",2)

