import os
import pandas as pd

m_dirs = os.listdir('scrap_res')
m_res = []
for m_dir in m_dirs:
    if os.path.splitext(m_dir)[1] != '.py':
        m_res.append(m_dir)
m_res = pd.DataFrame(m_res, columns=['city'])
print(m_res)
m_res.to_csv('../00_Data/info/city.CSV', index=False)
