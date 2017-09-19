import logging
import base64

from eduvpn.metadata import Metadata
from eduvpn.util import bytes2pixbuf, get_pixbuf
from eduvpn.config import icon_size
from eduvpn.manager import is_provider_connected
from eduvpn.steps.messages import fetch_messages


logger = logging.getLogger(__name__)


def select_profile(builder, list_, verifier, window):
    """called when a users selects a configuration"""
    notebook = builder.get_object('outer-notebook')
    switch = builder.get_object('connect-switch')
    ipv4_label = builder.get_object('ipv4-label')
    ipv6_label = builder.get_object('ipv6-label')
    twofa_label = builder.get_object('2fa-label')
    twofa_label_label = builder.get_object('2fa-label-label')
    name_label = builder.get_object('name-label')
    profile_label = builder.get_object('profile-label')
    profile_image = builder.get_object('profile-image')
    model, treeiter = list_.get_selected()
    if not treeiter:
        logger.info("no configuration selected, showing main logo")
        notebook.set_current_page(0)
        return
    else:
        uuid, display_name, icon, _ = model[treeiter]
        logger.info("configuration was selected {} ({})".format(display_name, uuid))
        meta = Metadata.from_uuid(uuid)
        name_label.set_text(display_name)
        if meta['icon_data']:
            icon = bytes2pixbuf(base64.b64decode(meta['icon_data'].encode()),
                                width=icon_size['width'] * 2, height=icon_size['height'] * 2)
        else:
            _, icon = get_pixbuf()
        profile_image.set_from_pixbuf(icon)
        profile_label.set_text(meta['connection_type'])
        connected = is_provider_connected(uuid=uuid)
        switch.set_state(bool(connected))
        if connected:
            ipv4, ipv6 = connected
            ipv4_label.set_text(ipv4)
            ipv6_label.set_text(ipv6)
        else:
            ipv4_label.set_text("")
            ipv6_label.set_text("")

        if meta.username:
            twofa_label.set_text(meta.username)
            twofa_label_label.set_text("2FA:")
        else:
            twofa_label.set_text("")
            twofa_label_label.set_text("")

        notebook.show_all()
        notebook.set_current_page(1)
        if meta.token:
            fetch_messages(meta=meta, builder=builder, verifier=verifier, window=window)
        return meta
