from flask import Flask, request, render_template
import re
import math
import os

app = Flask(__name__)

@app.route("/")
def loadPage():
    return render_template('index.html', query="")

@app.route("/", methods=['POST'])
def cosineSimilarity():
    try:
        universalSetOfUniqueWords = []
        matchPercentage = 0

        # Retrieve input query from form
        inputQuery = request.form['query']
        lowercaseQuery = inputQuery.lower()

        # Process query text
        queryWordList = re.sub("[^\w]", " ", lowercaseQuery).split()
        for word in queryWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        # Read and process database text
        with open("database1.txt", "r") as fd:
            database1 = fd.read().lower()
        databaseWordList = re.sub("[^\w]", " ", database1).split()
        for word in databaseWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        # Calculate term frequencies
        queryTF = []
        databaseTF = []

        for word in universalSetOfUniqueWords:
            queryTF.append(queryWordList.count(word))
            databaseTF.append(databaseWordList.count(word))

        # Compute dot product and magnitudes
        dotProduct = sum(q * d for q, d in zip(queryTF, databaseTF))
        queryVectorMagnitude = math.sqrt(sum(q ** 2 for q in queryTF))
        databaseVectorMagnitude = math.sqrt(sum(d ** 2 for d in databaseTF))

        # Calculate match percentage
        matchPercentage = (dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100 if queryVectorMagnitude and databaseVectorMagnitude else 0.0

        output = "Input query text matches %0.02f%% with database." % matchPercentage

        return render_template('index.html', query=inputQuery, output=output)
    except Exception as e:
        output = "Please Enter Valid Data"
        return render_template('index.html', query=inputQuery, output=output)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
