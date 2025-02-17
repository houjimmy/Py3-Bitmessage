About this fork
============

PyBitmessage is a little outdated, and the code can't compile well in newer systems. Because the app is a bit messy due to years of halting development, old version of the language and deprecated libraries, people were not trying to improve the software anymore. So, I will try to update de code using some tools like 2to3 using this tutorial: https://vallme2003.medium.com/how-to-use-python-2to3-converter-with-pycharm-ide-7114174995aa and doing everything else manually.

I've changed the version from 0.6 to 0.7 basically to show that the code is being/has been (in the time you read this) updated, but it is basically the same app. Today 26/11 I've already used the tool 2to3 to update all files. Now, I will start testing compiling again the code as is and fixing any problem; also, I will try to handle the issues with dynamically typing using python 3.5 and above type-hints, and see what can I do about the outdated QT3 libraries. But the main problem where I'm focusing now is the deprecated "pyelliptic" library that handles protocol-level calls, that I will try to replace with the "pyca/cryptography" library.

At the moment, I'm using PyCharm and Python 2to3 as tools. If you know something better or something that can make my life easier, please send me a message.

You are welcome to help me (seriously, I'm not very sure about what I am doing. I IMPLORE YOU!!!). Message me in BM-NBJ74QmJCct5i9F8aHtQBdNGcv8QGYDY . Our fork development channel is BM-2cVp51viwgf23cC6dt4jr9pSw1wfmHAaY1 , the Name/Passphrase is "py3bitmessage" (without the ""). 

I am also in the official bitmessage development chan, BM-2cWy7cvHoq3f1rYMerRJp8PT653jjSuEdY . See you all!


Everything from this point is from the old repository.


PyBitmessage
============

Bitmessage is a P2P communication protocol used to send encrypted messages to
another person or to many subscribers. It is decentralized and trustless,
meaning that you need-not inherently trust any entities like root certificate
authorities. It uses strong authentication, which means that the sender of a
message cannot be spoofed. BM aims to hide metadata from passive eavesdroppers 
like those ongoing warrantless wiretapping programs. Hence the sender and receiver 
of Bitmessages stay anonymous.


Development
----------
Bitmessage is a collaborative project. You are welcome to submit pull requests 
although if you plan to put a non-trivial amount of work into coding new
features, it is recommended that you first describe your ideas in the
separate issue.

Feel welcome to join chan "bitmessage", BM-2cWy7cvHoq3f1rYMerRJp8PT653jjSuEdY

References
----------
* [Project Website](https://bitmessage.org)
* [Protocol Specification](https://bitmessage.org/wiki/Protocol_specification)
* [Whitepaper](https://bitmessage.org/bitmessage.pdf)
* [Installation](https://bitmessage.org/wiki/Compiling_instructions)
* [Discuss on Reddit](https://www.reddit.com/r/bitmessage)
* [Chat on Gitter](https://gitter.im/Bitmessage/PyBitmessage)

