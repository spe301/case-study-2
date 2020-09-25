#!/usr/bin/env python
# coding: utf-8

# In[357]:


import sqlite3
conn = sqlite3.connect(r'C:\Users\aacjp\Downloads\northWind.sqlite')
cur = conn.cursor()


# In[358]:


product = cur.execute("""SELECT ProductName FROM Product ORDER BY ID;""").fetchall()


# In[359]:


price = cur.execute("""SELECT UnitPrice from OrderDetail""").fetchall()


# In[360]:


qnty = cur.execute("""SELECT Quantity from OrderDetail""").fetchall()


# In[361]:


len(qnty)


# In[362]:


ids = []
products = []
for i in range(len(cur.execute("""SELECT ID FROM Product;""").fetchall())):
    ids.append(cur.execute("""SELECT ID FROM Product;""").fetchall()[i][0])
    products.append(cur.execute("""SELECT ProductName FROM Product;""").fetchall()[i][0])


# In[363]:


product


# In[364]:


pids = []
for i in range(len(up)):
    pids.append(cur.execute("""SELECT ProductId FROM OrderDetail ORDER BY  ProductId;""").fetchall()[i][0])


# In[365]:


up = cur.execute("""SELECT UnitPrice FROM OrderDetail ORDER BY  ProductId;""").fetchall()


# In[366]:


qnty = cur.execute("""SELECT Quantity FROM OrderDetail ORDER BY  ProductId;""").fetchall()


# In[367]:


dollars = []
for i in range(len(up)):
    dollars.append(up[i][0] * qnty[i][0])


# In[368]:


pids[0], ids[0]


# In[369]:


import pandas as pd
pids = pd.DataFrame(pids)
up = pd.DataFrame(up)
dollars = pd.DataFrame(dollars)
df = pd.concat([pids, up, dollars], axis='columns')
df.columns = ['id', 'unitprice', '$spent']
df


# In[370]:


product_totals = []
for i in range(len(ids)):
    product_totals.append(sum(list(df.loc[df['id'] == ids[i]]['$spent'])))


# In[371]:


ro = []
for i in range(len(ids)):
    ro.append(cur.execute("""SELECT ReorderLevel FROM Product ORDER BY ID;""").fetchall()[i][0])


# In[372]:


ids = pd.DataFrame(ids)
products = pd.DataFrame(product)
total_dollars = pd.DataFrame(product_totals)
reorder_level = pd.DataFrame(ro)
new_df = pd.concat([ids, products, total_dollars, reorder_level], axis='columns')
new_df.columns = ['ids', 'products', 'total_dollars', 'reorder_level']
new_df


# Null Hypothesis: There is no correlation between total dollars and reorder level
# 
# Alternate Hypothesis: There is a correlation between total dollars and reorder level

# In[373]:


from matplotlib import pyplot as plt

plt.scatter(new_df['total_dollars'], new_df['reorder_level'])


# In[374]:


ro_list = list(np.unique(sorted(new_df['reorder_level'])))


# In[375]:


ro_list


# In[376]:


dro_dict = {}
for i in range(len(ro_list)):
    dro_dict[ro_list[i]] = list(new_df.loc[new_df['reorder_level'] == ro_list[i]]['total_dollars'])


# In[377]:


pops = []
for i in range(len(dro_dict)):
    pops.append(list(dro_dict.values())[i])


# In[378]:


def bootstrap(arr):
    n = 7
    return np.random.choice(list(arr), n, replace=True)


# In[379]:


import seaborn as sns

def make_list(arr):
    lsts = []
    for i in range(100000):
        lsts.append(np.mean(bootstrap(arr)))
    return lsts

def get_plot(arr):
    lsts = []
    for i in range(100000):
        lsts.append(np.mean(bootstrap(arr)))
    return sns.distplot(lsts)

def z_crit(lst, zmin, zmax):
    sigma = np.std(lst)
    mu = np.mean(lst)
    xmin = mu + (zmin * sigma)
    xmax = mu + (zmax * sigma)
    return xmin, xmax, mu


# In[380]:


mean = int(z_crit(make_list(pops[0]), -2, 2)[2])
get_plot(pops[0])
print(f'Reorder level = {ro_keys[0]}')
print(f'The average sample mean was {mean}')
mus = [mean]


# In[381]:


mean = int(z_crit(make_list(pops[1]), -2, 2)[2])
get_plot(pops[1])
print(f'Reorder level = {ro_keys[1]}')
print(f'The average sample mean was {mean}')
mus.append(mean)


# In[382]:


mean = int(z_crit(make_list(pops[2]), -2, 2)[2])
get_plot(pops[2])
print(f'Reorder level = {ro_keys[2]}')
print(f'The average sample mean was {mean}')
mus.append(mean)


# In[383]:


mean = int(z_crit(make_list(pops[3]), -2, 2)[2])
get_plot(pops[3])
print(f'Reorder level = {ro_keys[3]}')
print(f'The average sample mean was {mean}')
mus.append(mean)


# In[384]:


mean = int(z_crit(make_list(pops[4]), -2, 2)[2])
get_plot(pops[4])
print(f'Reorder level = {ro_keys[4]}')
print(f'The average sample mean was {mean}')
mus.append(mean)


# In[385]:


mean = int(z_crit(make_list(pops[5]), -2, 2)[2])
get_plot(pops[5])
print(f'Reorder level = {ro_keys[5]}')
print(f'The average sample mean was {mean}')
mus.append(mean)


# In[386]:


mean = int(z_crit(make_list(pops[6]), -2, 2)[2])
get_plot(pops[6])
print(f'Reorder level = {ro_keys[6]}')
print(f'The average sample mean was {mean}')
mus.append(mean)


# In[387]:


y = mus
x = ro_list
plt.scatter(x, y)


# In[388]:


sns.barplot(x, y)


# The barplot and scatterplot shown above do not indicate a correlation between total_dollars and reorder level

# I will extract the mean of all the mus, tot_mean. then I will see what percentage of dollar values are less than tot_mean where 
# reorder level = 0, and what percentages are more than tot_mean where reorder level = 30. the alpha is 0.05 so the percentages must both be >95 to prove h1 true.

# In[389]:


threshold = np.mean(mus)
n = len(dro_dict[ro_list[0]])
below = 0
for i in range(n):
    if dro_dict[ro_list[0]][i] < threshold:
        below += 1
        
percentage = 100 *below / n
booly = percentage >= 95
print(f'This indicates that h1 is {booly}, only {round(percentage, 2)}% is less than tot_mean')


# In[390]:


threshold = np.mean(mus)
n = len(dro_dict[ro_list[-1]])
above = 0
for i in range(n):
    if dro_dict[ro_list[-1]][i] > threshold:
        above += 1
        
percentage = 100 *above / n
booly = percentage >= 95
print(f'This indicates that h1 is {booly}, only {round(percentage, 2)}% exceeds tot_mean')


# This already appears to be enough to prove h0 true and h1 false. where order level = 0, 54.17% of the data exceeds the mean and that number actually decreases to 37.5% and that is not enough to show a negative correlation either

# In[391]:


np.mean(dro_dict[ro_list[0]]), np.mean(dro_dict[ro_list[-1]])


# In[392]:


np.mean(dro_dict[ro_list[1]]), np.mean(dro_dict[ro_list[-2]])


# I am not finding any correlation but I will preform anova just to make sure

# In[393]:


new_df


# In[394]:


import scipy
scipy.stats.f_oneway(new_df['total_dollars'], new_df['reorder_level'])


# given that p-value > 0.05 I will double check for negative correlation with a tukey test

# In[395]:


from statsmodels.stats.multicomp import pairwise_tukeyhsd

# perform multiple pairwise comparison (Tukey HSD)
m_comp = pairwise_tukeyhsd(endog=new_df['total_dollars'], groups=new_df['reorder_level'], alpha=0.05)
print(m_comp)


# In[ ]:




