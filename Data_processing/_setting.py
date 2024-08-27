class set_connect:
    def __init__(self):
        self.influxdb_org = "org100"
        self.influxdb_url = "http://localhost:9999"
        self.influxdb_bucket = "bucket100"
        
    
    def influxdb_token(self, whichtoken):
        if whichtoken == "super":
            # 家
            super_token = ""
            # 學校
            super_token = "PkIU2qWd2Dfa_VqEyOC8YS24PkZHwg3lAOjXAhVpg_W8MJWx7qCnZLdiDdUCKwxAIHv91wX8tD0CabD4z1_9oA=="
            return super_token
            
        if whichtoken == "custom":
            # 家
            custom_token = "2xE_ttHl9rzs0p19VzPwFdnsbVMp-jZwi7W4SKNTyiZXWvmFOPPN-wD9ZpvrLKsKC4YxooBN4o949ZFC6a70PQ=="
            # 學校
            custom_token = "7QWmjsZKU9E3cEdIp5JAs6vUzdfJ03O9YJl45I7e9rY1uol4AoswJAxhIJ21sdFdyrQo96YbIOIkQmbp-h5EqQ=="
            return custom_token
        
