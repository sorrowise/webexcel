# Excel 文件处理工具

基于 Pyodide 的 Excel 文件处理工具，完全在浏览器中运行，无需服务器。

## 功能特点

- ✅ 完全在浏览器中运行，无需服务器
- ✅ 使用 pandas 处理 Excel 文件
- ✅ 业务逻辑与前端代码分离，易于定制
- ✅ 支持拖拽上传文件
- ✅ 支持批量处理多个文件
- ✅ 单文件分发，只需分享 HTML 文件

## 使用方法

### 基本使用

1. 在浏览器中打开 `index.html` 文件
2. 等待 Pyodide 环境加载完成（首次加载可能需要一些时间）
3. 点击上传区域或拖拽 Excel 文件到页面
4. 点击"开始处理"按钮
5. 处理完成后，点击下载链接保存处理后的文件

### 定制业务逻辑

要修改处理逻辑，只需编辑 `process.py` 文件中的 `process_excel` 函数：

```python
def process_excel(file_path):
    # 读取 Excel 文件
    df = pd.read_excel(file_path)
    
    # 在这里添加您的业务逻辑
    # 例如：数据筛选、排序、计算等
    
    # 生成输出文件名
    output_path = f"{base_name}_processed.xlsx"
    
    # 保存处理后的文件
    df.to_excel(output_path, index=False)
    
    return output_path
```

### 常见处理示例

#### 1. 数据筛选
```python
df = df[df['销售额'] > 1000]
```

#### 2. 数据排序
```python
df = df.sort_values('日期', ascending=False)
```

#### 3. 添加计算列
```python
df['总价'] = df['单价'] * df['数量']
```

#### 4. 数据分组统计
```python
grouped = df.groupby('类别').agg({'销售额': 'sum', '数量': 'mean'})
```

#### 5. 数据清洗
```python
df = df.dropna()  # 删除空值
df = df.drop_duplicates()  # 删除重复行
```

#### 6. 处理多个工作表
如果您的 Excel 文件包含多个工作表，可以使用 `process_excel_multisheet` 函数作为参考。

## 文件结构

```
.
├── index.html      # 主 HTML 文件（包含前端 UI 和 Pyodide 集成）
├── process.py      # 可定制的 Python 业务逻辑文件
└── README.md       # 说明文档
```

## 分发方式

由于所有处理都在浏览器中完成，您只需要：

1. 将 `index.html` 和 `process.py` 放在同一目录下
2. 通过 HTTP 服务器访问（不能直接打开文件，需要使用本地服务器）

### 使用 Python 启动本地服务器

```bash
# Python 3
python -m http.server 8000

# 然后在浏览器中访问
http://localhost:8000
```

### 使用 Node.js 启动本地服务器

```bash
# 安装 http-server
npm install -g http-server

# 启动服务器
http-server -p 8000

# 然后在浏览器中访问
http://localhost:8000
```

## 注意事项

1. **首次加载**：Pyodide 环境首次加载需要下载约 10MB 的文件，可能需要一些时间
2. **浏览器兼容性**：建议使用现代浏览器（Chrome、Firefox、Edge 等）
3. **文件大小**：由于在浏览器中运行，建议处理较小的 Excel 文件（< 10MB）
4. **网络要求**：首次使用需要网络连接以下载 Pyodide 和 pandas 库
5. **本地服务器**：由于浏览器的安全限制，必须通过 HTTP 服务器访问，不能直接打开 HTML 文件

## 技术栈

- **Pyodide**: 在浏览器中运行 Python
- **pandas**: 数据处理库
- **openpyxl**: Excel 文件读写库

## 许可证

MIT License
