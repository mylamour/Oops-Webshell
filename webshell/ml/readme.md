* 采用了 ![Text-CNN-Classification](https://github.com/dennybritz/cnn-text-classification-tf/_)该神经网络，通过对文本预处理之后，初步对文本进行分类。
* 读了下论文，觉得机器学习的方法还是比较适用的。
* 但样本数较少，所以结果应该有问题。同时可能有其他意向不到的问题。且把代码做一行文本看待后，进行处理。会导致需要大量的内存占用(在我本机上是内存耗尽导致崩溃)。具体可以详细阅读该CNN网络的设计，由于数组过大所致。
* 仍需改进，等训练后上传model (已上传)

> 修改predict内的文件夹路径为你自定义的路径，然后运行脚本即可，方法如下。

```bash
	
chmod +x predict.sh
./predict.sh

```
