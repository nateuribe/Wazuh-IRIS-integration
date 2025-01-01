# Wazuh-IRIS-integration
Simple (**Unofficial**) Wazuh integration to send alerts to IRIS, as described in [https://nateuribe.tech/blog/foss-soc/](https://nateuribe.tech/blog/foss-soc/).

> [!NOTE]
> As of 2024-07-03, there is now [official documentation](https://wazuh.com/blog/enhancing-incident-response-with-wazuh-and-dfir-iris-integration/) by Wazuh for integrating IRIS with Wazuh. I **highly recommend** that you follow that documentation instead.


## Requirements
- [Wazuh](https://github.com/wazuh/wazuh) Server
- [IRIS](https://github.com/dfir-iris/iris-web)
- Python
- python-requests

## Installation
> [!IMPORTANT]
> By default, the IRIS Docker container utilizes self-signed certificates (https://docs.dfir-iris.org/operations/configuration/#certificates).
> If your setup is utilizing self-signed certificates, you will need to disable certificate verification with `verify=False`:
> ```python
> response = requests.post(hook_url, verify=False, data=payload, headers={"Authorization": "Bearer " + api_key, "content-type": "application/json"})
> ```

```
git clone https://github.com/nateuribe/Wazuh-IRIS-integration.git
cd Wazuh-IRIS-integration/
cp custom-iris.py /var/ossec/integrations/custom-iris.py
chmod 750 /var/ossec/integrations/custom-iris.py
chown root:wazuh /var/ossec/integrations/custom-iris.py
```
Add the following snippet into the `/var/ossec/etc/ossec.conf` config file:
```xml
<!-- ... Rest of config ... -->

<!-- IRIS integration -->
<integration>
  <name>custom-iris.py</name>
  <hook_url>http://IRIS-BASE-URL/alerts/add</hook_url>
  <level>7</level>
  <api_key>APIKEY</api_key>
  <alert_format>json</alert_format>
</integration>

<!-- ... Rest of config ... -->
```
Adjust `<hook_url>` and `<api_key>` to your environment, and change `<level>` to the desired threshold for alerts.

Restart the `wazuh-manager` service after making the above settings.

The IRIS API can be found in the Dashboard under **My Settings**.

### IRIS versions 2.4.x<
Since [IRIS 2.4.6](https://github.com/dfir-iris/iris-web/releases/tag/v2.4.6), you will need to add your IRIS user to the customer for which you are ingesting alerts for to see new entries in the alerts tab.

This can be configured by navigating to `Advanced` -> `Access Control` under **Manage** on the left panel, clicking on your user under **Users**, clicking on the **Customers** tab, and then **Manage** to add the customer (should be **IrisInitialClient** by default on a base install).

## Configuration

The script comes preconfigured with a basic payload to create new IRIS alerts.
Use the Alerts API reference to modify this at will (https://docs.dfir-iris.org/latest/_static/iris_api_reference_v2.0.4.html#tag/Alerts/operation/post-case-add-alert).

Here are some notable values you may change:

`alert_source_link` - URL from where the alert came from (Wazuh in this instance).

`alert_note` - Note or comment to add to each alert.

`alert_customer_id` - Alerts in IRIS get assigned to "customers"; this is the ID of the customer for which the alerts pertains to.
