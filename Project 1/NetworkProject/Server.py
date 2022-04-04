from socket import *
import pandas as pd
import os

serverPort = 8000
serverSocket = socket(AF_INET, SOCK_STREAM)  # Defining a TCP server.
serverSocket.bind(('', serverPort))  # Assign the server to port number 3000.
serverSocket.listen(1)  # Listen for requests.

print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()  # Get the request and its IP and Port numbers.
    sentence = connectionSocket.recv(1024).decode()  # Decode the request.
    print(addr)  # Print address of the request (IP and Port numbers).
    print(sentence)  # Print HTTP request information.

    url = sentence.split()[1]  # Get the requested page.
    if (url == '/') or (url == '/index.html'):
        index = open('index.html')
        indexCode = index.read()  # Read the index.html file.
        index.close()  # Close the file.
        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())  # Tell the client that everything is ok and the page is sent.
        connectionSocket.send('Content-Type: text/html \r\n'.encode())  # Set the type to HTML page.
        connectionSocket.send('\r\n'.encode())  # End of the header of the response.
        connectionSocket.send(indexCode.encode())  # Send HTML code after encoding.
    elif url.endswith('.jpg') or url.endswith('.jpg/') or url.endswith('.png') or url.endswith('.png/'):
        imageName = url.split('/')[1]  # Get image name.
        imageType = imageName.split('.')[1]  # Get image type.
        if imageType == 'jpg':  # For .jpg images the content-type in header must be jpeg.
            imageType = 'jpeg'
        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
        connectionSocket.send(('Content-Type: image/' + imageType + ' \r\n').encode())  # Set image type.
        connectionSocket.send('\r\n'.encode())
        imagePath = os.path.join('images', imageName)
        image = open(imagePath, 'rb')
        imageData = image.read()
        image.close()
        connectionSocket.send(imageData)
    elif url == "/sortName" or url == "/sortName/":
        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
        connectionSocket.send('Content-Type: text/plain \r\n'.encode())  # Sending plain text.
        connectionSocket.send('\r\n'.encode())
        data = pd.read_csv('data.csv')  # Read the csv file that is to be sorted depending on name.
        names = data.iloc[:, 0].values  # Get names field as an array.
        prices = data.iloc[:, 1].values  # Get prices field as an array.
        # Sort the two array depending on the name in an ascending order.
        for i in range(0, len(names)):
            for j in range(i + 1, len(names)):
                if names[j] < names[i]:
                    names[i], names[j] = names[j], names[i]
                    prices[i], prices[j] = prices[j], prices[i]
        numberOfSpaces = 50  # Defining a fixed number of spaces that will split the 2 columns that will be sent to the client.
        message = "Names" + " " * (numberOfSpaces - 5) + "| Prices\n"  # Put titles to the columns.
        for i in range(0, len(names)):  # Add each name under names column and each price under prices column.
            message += str(names[i]) + " " * (numberOfSpaces - len(names[i])) + "| " + str(prices[i]) + "\n"
        connectionSocket.send(message.encode())  # Send the sorted data as a plain text.
    elif url == "/sortPrice" or url == "/sortPrice/":
        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
        connectionSocket.send('Content-Type: text/plain \r\n'.encode())
        connectionSocket.send('\r\n'.encode())
        data = pd.read_csv('data.csv')
        names = data.iloc[:, 0].values
        prices = data.iloc[:, 1].values
        for i in range(0, len(prices)):
            for j in range(i + 1, len(prices)):
                if prices[j] < prices[i]:
                    names[i], names[j] = names[j], names[i]
                    prices[i], prices[j] = prices[j], prices[i]
        numberOfSpaces = 50
        message = "Names" + " " * (numberOfSpaces - 5) + "| Prices\n"
        for i in range(0, len(prices)):
            message += str(names[i]) + " " * (numberOfSpaces - len(names[i])) + "| " + str(prices[i]) + "\n"
        connectionSocket.send(message.encode())
    else:
        notFound = open('404.html')
        notFoundCode = notFound.read()  # Read the 404 Not Found error HTML page.
        notFound.close()
        # Add the IP and Port numbers of the client to the HTML code at their predefined places that are ? (Replace first ? by the IP and second ? by the port number).
        index = notFoundCode.index("?")
        firstPart = notFoundCode[0:index]
        secondPart = notFoundCode[index + 1:]
        notFoundCode = firstPart + str(addr[0]) + secondPart
        index = notFoundCode.index("?")
        firstPart = notFoundCode[0:index]
        secondPart = notFoundCode[index + 1:]
        notFoundCode = firstPart + str(addr[1]) + secondPart

        connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode())  # Tell the client that the page not found with code 404.
        connectionSocket.send('Content-Type: text/html \r\n'.encode())
        connectionSocket.send('\r\n'.encode())
        connectionSocket.send(notFoundCode.encode())  # Send the page.
    connectionSocket.close()  # Close the connection.
