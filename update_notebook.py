import json
import os
import sys

target = 'process data analysis on nonlinearity.ipynb'

try:
    f = open(target, 'r', encoding='utf-8')
    content = f.read()
    f.close()
    
    data = json.loads(content)

    source_to_find = [
        "        # metric\n",
        "        if (condition_2 == True) & (condition_3 == False):\n",
        "            data_file[\"metric\"] = data_file[\"metric_lut\"]\n",
        "        elif (condition_2 == True) & (condition_3 == True):\n",
        "            data_file[\"metric\"] = data_file[\"metric_max\"]\n",
        "        else:\n",
        "            data_file[\"metric\"] = data_file[['bod_psi_1', 'cod_psi_1']].max()\n"
    ]

    replacement = [
        "        # metric selection using vectorized logic\n",
        "        metric_conditions = [\n",
        "            (condition_2 == True) & (condition_3 == False),\n",
        "            (condition_2 == True) & (condition_3 == True)\n",
        "        ]\n",
        "        metric_choices = [\n",
        "            data_file[\"metric_lut\"],\n",
        "            data_file[\"metric_max\"]\n",
        "        ]\n",
        "        default_metric = data_file[['bod_psi_1', 'cod_psi_1']].max(axis=1)\n",
        "        \n",
        "        data_file[\"metric\"] = np.select(metric_conditions, metric_choices, default=default_metric)\n"
    ]

    modified = False
    for cell in data.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            for i in range(len(source) - len(source_to_find) + 1):
                if source[i:i+len(source_to_find)] == source_to_find:
                    source[i:i+len(source_to_find)] = replacement
                    modified = True
                    break

    if modified:
        output_str = json.dumps(data, indent=1)
        fw = open(target, 'w', encoding='utf-8')
        fw.write(output_str)
        fw.flush()
        fw.close()
        print("DONE")
    else:
        print("NOT_FOUND")

except Exception as e:
    print(str(e))
