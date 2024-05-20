from flask import Flask, jsonify, request

app = Flask(__name__)

playlists = { }

@app.route('/playlist/create', methods=['POST'])
def create_playlist():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    playlist_id = str(len(playlists) + 1)
    playlists[playlist_id] = {'name': name, 'description': description}
    return jsonify({'playlist_id': playlist_id}), 201

@app.route('/playlist/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    playlist = playlists.get(playlist_id)
    if playlist:
        return jsonify(playlist)
    else:
        return jsonify({'error': 'Playlist not found'}), 404

@app.route('/playlist/update/<playlist_id>', methods=['PUT'])
def update_playlist(playlist_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    if playlist_id in playlists:
        playlists[playlist_id]['name'] = name
        playlists[playlist_id]['description'] = description
        return jsonify({'message': 'Playlist updated successfully'}), 200
    else:
        return jsonify({'error': 'Playlist not found'}), 404

@app.route('/playlist/delete/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    if playlist_id in playlists:
        del playlists[playlist_id]
        return jsonify({'message': 'Playlist deleted successfully'}), 200
    else:
        return jsonify({'error': 'Playlist not found'}), 404
    

@app.route('/playlist/<playlist_id>/add_song', methods=['POST'])
def add_song_to_playlist(playlist_id):
    data = request.get_json()
    title = data.get('title')
    artist = data.get('artist')
    if playlist_id in playlists:
        if 'songs' not in playlists[playlist_id]:
            playlists[playlist_id]['songs'] = []
        playlists[playlist_id]['songs'].append({'title': title, 'artist': artist})
        return jsonify({'message': 'Song added to playlist successfully'}), 200
    else:
        return jsonify({'error': 'Playlist not found'}), 404
    
@app.route('/playlist/<playlist_id>/remove_song/<song_id>', methods=['DELETE'])
def remove_song_from_playlist(playlist_id, song_id):
    if playlist_id in playlists:
        if 'songs' in playlists[playlist_id]:
            if int(song_id) < len(playlists[playlist_id]['songs']):
                del playlists[playlist_id]['songs'][int(song_id)]
                return jsonify({'message': 'Song removed from playlist successfully'}), 200
            else:
                return jsonify({'error': 'Song not found'}), 404
        else:
            return jsonify({'error': 'No songs in playlist'}), 404
    else:
        return jsonify({'error': 'Playlist not found'}), 404
    
@app.route('/playlist/search_song', methods=['GET'])
def search_song():
    artist = request.args.get('artist')
    results = []
    for playlist_id, playlist in playlists.items():
        if 'songs' in playlist:
            for song in playlist['songs']:
                if song['artist'] == artist:
                    results.append({'playlist_id': playlist_id, 'song': song})
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)


# cant for the life of me figure out the issue with the add_song_to_playlist function, its the same thing as the others but it keeps returning a 404 error
# i dont know if the remove_song_from_playlist function works because i cant get the add_song_to_playlist function to work
# the search_song function works fine, at least i think it does because it showed an empty list which is what i expected
# the other functions work fine, i tested them with postman and they work as expected
# hopefully you can help me figure out the issue with the add_song_to_playlist function
# thank you for your time and help
# i appreciate it