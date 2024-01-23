
yaml_template = """heartbeat.monitors:{% for index, row in data.iterrows() %}
- type: {{ row['type'] }}
  id: {{ row['id'] }}
  name: {{ row['name'] }}
  enabled: true
  schedule: '@every 60s'
  hosts: {% for host in row['hosts'].split(', ') %}
  - {{ host }} {% endfor %}
  ipv4: {{ row['ipv4'] }} #user inputs
  ipv6: {{ row['ipv6'] }}
  fields_under_root: true
  fields:
    geo:
      city_name: {{ row['city_name'] }}
      country_iso_code: {{ row['country iso code'] }}
      country_name: {{ row['country name'] }}
      location:
        lat: {{ row['latitude'] }}
        lon: {{ row['longitude'] }}
      name: {{ row['geo.name'] }}
      location_id: {{ row['location id'] }}
    network:
      site_id: {{ row['site id'] }}
      site_name: {{ row['site name'] }}
      site_uid: {{ row['site uid'] }}
      site_category: {{ row['site category'] }}
    cmdb:
      ci_name: {{ row['cmbd ci name'] }}
      ci_uid: {{ row['cmdb ci uid'] }}
      ci_parent_name: {{ row['cmdb ci parent name'] }}
      ci_parent_uid: {{ row['cmdb ci parent uid'] }}
      event_category: {{ row['cmdb event category'] }}

  keep_null: true
  mode: {{ row['mode'] }}
  timeout: {{ row['timeout'] }}
  wait: {{ row['wait'] }}
  tags: {{ row['tags'] }}
{% endfor %}
"""