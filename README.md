## A Simple Text Search Engine


这是一个简单的文本搜索引擎的雏形，它的实现来自[Quora](http://www.quora.com/I-am-confident-that-I-am-going-to-build-a-search-engine-that-will-compete-with-Google-at-least-in-the-smallest-scale-possible-first-but-for-now-I-dont-know-any-programming-What-should-I-do)上一个人提出的有趣的问题，意思大概就是，我现在什么都不会，甚至我不会编程，但是我有信心能够在未来建造一个搜索引擎可以与google匹敌．回复的帖子有人对其嘲讽的，＂你连20米都没有跑过，却想赢得马拉松吗？＂，但是其中也有热心与任性的外国网友给出了一些搜索引擎的原理．

诚然，想构造一个与google匹敌的search engine并不容易，但是运用一些简单的编程技巧与少量的数学公式，我们可以构造出一个简单的文本搜索引擎．在这个小作品中，我就实现了一个这样简易的文本索索引擎，可以实现搜索功能，并且给出一个具有排名的结果列表（search and rank）．

其中的思想却及其简单，首先我们需要构造一个inverted index，这个index的实质其实就是一个哈希表，它可以根据一个单词返回这个单词出现过的文件列表．有了这样一个数据结构，我们就可以实现search部分的功能了．

接下来，核心则是如何实现一个rank功能？这里我决定用比较简单的[tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) rank方法．该方法可以实现对search后的结果进行一个rank功能然后再输出列表．关于这个部分的核心数学原理可以在[这篇博客](http://www.ruanyifeng.com/blog/2013/03/tf-idf.html)中一探究竟．

最终，这个简易的文本搜索引擎可以实现基本的三个功能（目前仅限查找英文document）：

1. 实现单个单词的search

2. 实现一个query string的查找，但是不区分单词的先后顺序

3. 实现一个query string的查找，但是结果时严格保证search到的是与query单词出现顺序严格一致．该功能类似于在搜索引擎中对关键词两边加双引号的效果．

## License

This project is under [GPL License](http://www.gnu.org/licenses/gpl.txt)

