# -*- coding: utf-8 -*-
# @Date    : 2016/12/3
# @Author  : hrwhisper
import codecs
import sys
from collections import Counter
from optparse import OptionParser
from multiprocessing import Pool
import jieba
from sklearn.externals import joblib
from model_manage import BowTransform
import time
import json
from flask import Flask, request, render_template


def token(x):
    return Counter(jieba.lcut(x))


def judgesms():
# if __name__ == '__main__':
    # parser = OptionParser()
    # parser.add_option('-c', '--classifier', dest="cls_name", type='string', default='p',
    #                   help="define the classifier you want to use:  \t\t\n"
    #                        "p  => Perceptron,\t\t\t\t\t\n"
    #                        "lr => LogisticRegression,\t\t\t\t\t\n"
    #                        "nb => NaiveBayesian,\t\t\t\t\t\n"
    #                        "svm => SVM(sklearn),\t\t\t\t\t\n"
    #                        "lrs => LogisticRegression(sklearn),\t\t\t\t\t\n"
    #                        "nbs => NaiveBayesian(sklearn),")
    #
    # parser.add_option('-i', '--input', dest="input_filename", type='string', default='./data/单条垃圾短信.txt',
    #                   help="input file name")
    #
    # parser.add_option('-o', '--output', dest="output_filename", type='string', default='./data/result.txt',
    #                   help="output file name")
    #
    # options, args = parser.parse_args()
    #
    classifiers = {
        'p': './model/Perceptron.pkl',  # 0.1 2000
        'lr': './model/LogisticRegression.pkl',  # 0.2 2000
        'nb': './model/NaiveBayesian.pkl',  # 0.00241
        'svm': './model/SVM_sklearn.pkl',
        'lrs': './model/Logistic_sklearn.pkl',
        'nbs': './model/Bayes_sklearn.pkl'
    }
    #
    cls_name = 'p'
    # file_path = options.input_filename
    # out_path = options.output_filename

    if cls_name not in classifiers.keys():
        print('check your classifiers name, you can use -h for help')
        sys.exit()

    start = time.time()
    jieba.initialize()
    # try:
    #     with codecs.open(file_path, 'r', 'utf-8') as f:
    #         data = [line.strip() for line in f.read().split('\n')]
    #         if data[-1] == '':
    #             data.pop()
    # except FileNotFoundError as e:
    #     print('Please check your input filename')
    #     sys.exit()
    data = ['【团油】赠您128元加油券包已到账，加油立即可用！官方信息，谨防失效 t.ctyxxjs.cn/jEuZF 回T取关']
    # data = [Counter(d) for d in map(jieba.cut, data)]
    data = Pool().map(token, data)
    print('end token in {}\n'.format(time.time() - start))
    cv = BowTransform.load_vsm()
    data = cv.transform(data)
    print('end bow in {}\n'.format(time.time() - start))
    cls = joblib.load(classifiers[cls_name])
    predicted = cls.predict(data)
    print(predicted[0])
    value = predicted[0]
    # with open(out_path, 'w+') as f:
    #     for x in predicted:
    #         f.write(str(x) + '\n')
    print('task complete. total time: {}\n using {}'.format(time.time() - start, cls))
    if value == 1:
        return True
    return False

# if __name__ == '__main__':
#     judgesms()

# flask服务
app = Flask(__name__)

app.config["JSON_AS_ASCII"] = False
@app.route("/",methods=['GET','POST'])
def index():
    return json.dumps({'message': 'hello internal'})
@app.route("/getrequest",methods=['GET','POST'])
def getrequest():
    val = request.get_json()
    app.logger.info(val['data']['name'])
    # app.logger.info(judgesms())
    result = judgesms()
    # return json.dumps({'data':[1],'success':'true'})
    return json.dumps({'data':result,'success':'true'})

if __name__ == '__main__':
    # 默认访问：http://127.0.0.1:8888/
    app.run(debug=True, host='127.0.0.1', port=8080)