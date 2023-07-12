from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def sort_posts():
    """
        Sort the posts based on the provided query parameters.

        Query Parameters:
        - sort (str): The field to sort by ('title' or 'content').
        - direction (str): The sorting direction ('asc' or 'desc').

        Returns:
        - JSON response containing the sorted posts or the original posts if parameters are missing or invalid.
        """
    sort_by = request.args.get('sort')
    direction = request.args.get('direction', '').lower()

    sort_fields = {'title', 'content'}
    direction_fields = {'asc', 'desc'}

    if sort_by and direction:
        if sort_by not in sort_fields or direction not in direction_fields:
            return jsonify({"error": "Invalid sort field or direction"}), 400

        sorted_posts = sorted(POSTS, key=lambda x: x[sort_by], reverse=(direction == 'desc'))
        return jsonify(sorted_posts)

    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_posts():
    """
    Adds a new post

    Returns:
        New JSON response containing list of added post and HTTP status code
    """
    title = request.json.get('title')
    content = request.json.get('content')
    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400
    max_id = max([post['id'] for post in POSTS]) if POSTS else 0
    new_post = {
        "id": max_id + 1,
        "title": title,
        "content": content
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_posts(post_id):
    """
    Delete a post with the specified ID

    Args:
        post_id

    Returns:
        A message to confirm post deleted with post ID and HTTP status code
    """
    post_delete = None
    for post in POSTS:
        if post['id'] == post_id:
            post_delete = post
            break
    if post_delete:
        POSTS.remove(post_delete)
        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

    return jsonify({"error": "Post not found"}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update post with specified ID

    Args:
        post_id

    Returns:
        New JSON response containing list of updated title and content
    """
    for post in POSTS:
        if post['id'] == post_id:
            new_title = request.json.get('title', post['title'])
            new_content = request.json.get('content', post['content'])

            post['title'] = new_title
            post['content'] = new_content

            updated_post = {
                "id": post_id,
                "title": new_title,
                "content": new_content
            }
            return jsonify(updated_post), 200
    return jsonify({"error": "Post not found"}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """
        Search for posts based on title and content parameters.

        Query Parameters:
        - title (str): The title to search for.
        - content (str): The content to search for.

        Returns:
        - JSON response containing the list of matching posts.
        """
    title = request.args.get('title')
    content = request.args.get('content')

    if not title and not content:
        return jsonify([])

    searched_post = [post for post in POSTS
                     if (title in post['title'].lower()) or (content in post['content'].lower())]

    return jsonify(searched_post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
