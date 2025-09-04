#pip install requests

'''import requests
baseUrl='https://jsonplaceholder.typicode.com'
posts_response = requests.get(f'{baseUrl}/posts/1')
posts = posts_response.json()
print(posts)
#print(posts[1])
'''

# pip install requests 

import requests 
baseUrl = 'https://jsonplaceholder.typicode.com'

# read all posts : GET /posts 
print('Consuming : Read All Posts...')
response = requests.get(f'{baseUrl}/posts')
posts = response.json()
print(posts)

# read by id : GET /posts/1
print('Consuming : Read Post By Id == 1...')
response = requests.get(f'{baseUrl}/posts/1')
post = response.json()
print(post)

# create post : POST /posts {"userId":1, "title":"Some Title", "body" : "Some Body"}
print('Consuming : create post...')
post = {"userId":1, "title":"Some Title", "body" : "Some Body"}
response = requests.post(f'{baseUrl}/posts', data = post)
createdPost = response.json()
print(createdPost)