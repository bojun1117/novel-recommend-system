import torch
import jieba.analyse
from transformers import BertConfig, BertTokenizer, BertForSequenceClassification


def to_input_id(sentence_input):
  return tokenizer.build_inputs_with_special_tokens(tokenizer.convert_tokens_to_ids(tokenizer.tokenize(sentence_input)))

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
config = BertConfig.from_pretrained('trained_model/config.json')
model = BertForSequenceClassification.from_pretrained('trained_model/pytorch_model.bin',config=config)
model.eval()
pcount = 0
ncount = 0
dict_key = {}
target='蠱真人'   #目標書名

with open('comment.txt','r',encoding='utf-8') as f:
    sentences = f.readlines()
    for s in sentences:
        s = s.strip()
        input_id = to_input_id(s)
        assert len(input_id) <= 512
    
        while len(input_id)<512:
          input_id.append(0)
        input_ids = torch.LongTensor(input_id).unsqueeze(0)
    
        outputs = model(input_ids)
        predicts = outputs[:2]
        predicts = predicts[0]
        max_val = torch.max(predicts)
        predict_label = (predicts == max_val).nonzero().numpy()[0][1]
        if str(predict_label) == '1':
          pcount = pcount +1
        else:
          ncount = ncount +1
        ks = jieba.analyse.extract_tags(s, topK=4)
        for index in ks:
          if index not in dict_key:
            dict_key.setdefault(index,1)
          else:
            dict_key[index] = dict_key.get(index) + 1

score = round(pcount*5/len(sentences),2)
if score >= 4:
  recom = '推薦'
elif score >= 3:
  recom = '尚可'
else:
  recom = '不推'

k1 = max(dict_key,key=dict_key.get)
novelname = target+'output.txt'

with open(novelname,'w',encoding='utf-8') as o:
  o.writelines('書名： '+str(target))
  o.writelines('\n正面評論數：'+str(pcount)+'\n負面評論數：'+str(ncount))
  o.writelines("\n評分：5/"+str(score)+'   '+str(recom))
  o.writelines('\n關鍵字： '+str(k1))

print('書名： '+target)
print("pcount=",pcount)
print("ncount=",ncount)
print("評分：5/"+str(score)+'   '+recom)
print('關鍵字： '+k1)

