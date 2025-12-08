import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from tokenizer import Tokenizer # 昨日建立的函式庫

negative_words = ["disappointed", "sad", "frustrated", "painful", "worried", "angry"]
positive_words = ["happy", "successful", "joyful", "lucky", "love", "hopeful"]

# 建立初始值
all_words = negative_words + positive_words
tokenizer = Tokenizer(all_words, special_token = ['[UNK]','[PAD]'], max_len = 1)
token2num, num2token = tokenizer.token2num, tokenizer.num2token

input_data = torch.tensor([token2num[i] for i in negative_words + positive_words])
labels = len(negative_words) * [[1., 0.]] + len(positive_words) * [[0., 1.]]
labels = torch.tensor(labels)
print('第0筆訓練資料:', input_data[0])
print('第0筆訓練標籤:', labels[0])

class EmbDNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, output_size, padding_idx):
        super().__init__()
        self.embedding = nn.Embedding(
                                num_embeddings = vocab_size, 
                                embedding_dim = embedding_dim,
                                padding_idx = padding_idx

                             )
        
        self.fc = nn.Linear(embedding_dim, output_size)

    def forward(self, x):
        embedded = self.embedding(x)
        out = self.fc(embedded)  
        return out

    
vocab_size = len(token2num)       # 詞彙表大小
embedding_dim = 2                 # 詞嵌入層维度
output_size = 2                   # 輸出大小（分類數量）
padding_idx = token2num['[PAD]']  # 取得PAD索引

model = EmbDNN(vocab_size, embedding_dim, output_size, padding_idx)

# 定義損失函數與優化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

loss_record = []
epochs = 30000
for epoch in range(epochs):
    # 梯度初始化
    optimizer.zero_grad()
    # 前向傳播計算答案
    outputs = model(input_data)
    # Loss計算損失
    loss = criterion(outputs, labels)
    loss_record.append(loss)        # 紀錄該次Epoch的損失值
    
    # 反向傳播計算梯度
    loss.backward()
    # 優化器更新權重
    optimizer.step()
    # 每訓練1000次顯示Loss值
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item()}')

def show_training_loss(train_loss):
    fi_los = [fl.item() for fl in train_loss ]
    plt.plot(fi_los)
    #標題
    plt.title('Result')
    #y軸標籤
    plt.ylabel('Loss')
    #x軸標籤
    plt.xlabel('Epoch')
    #顯示折線的名稱
    plt.legend(['train'], loc='upper left')
    #顯示折線圖
    plt.show()

show_training_loss(loss_record)        

embedding_layer = model.embedding
embedding_weights = embedding_layer.weight.data
torch.save(embedding_weights, 'embedding_weights.pth')

def visualization(embedding_matrix, num2token):
    
    # 提取降維後的坐標
    x_coords = embedding_matrix[:, 0]
    y_coords = embedding_matrix[:, 1]

    # 繪製詞嵌入向量的散點圖
    plt.figure(figsize=(10, 8))
    plt.scatter(x_coords, y_coords)

    # 標註散點
    for i in range(len(embedding_matrix)):
        plt.annotate(num2token[i], (x_coords[i], y_coords[i]))
        
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    plt.title('Visualization of Embedding Vectors')
    plt.show()


token_nums = [i for i in num2token] 
token_nums = torch.tensor(token_nums)
emb = nn.Embedding(len(token_nums), 2)
loaded_embedding_weights = torch.load('embedding_weights.pth')
emb.weight = nn.Parameter(loaded_embedding_weights)
embedding_vector = emb(token_nums).detach().numpy()
visualization(embedding_vector, num2token)
