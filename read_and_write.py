#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

def get_json_data(file_path: str, key: str, value: str) -> None:
    dicts: Dict[Union[str,int],Union[str, int]] = {}

    with open(file_path,"r+",encoding='utf-8') as fp:
        json_data = json.load(fp)
        # clear file, pointer offset
        fp.seek(0)
        fp.truncate()
        json_data[key] = value
        dicts = json_data

        json.dump(dicts, fp, ensure_ascii=False)
