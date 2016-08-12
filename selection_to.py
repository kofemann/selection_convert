import terminatorlib.plugin as plugin
import gtk
from terminatorlib.translation import _
from datetime import timedelta, datetime

AVAILABLE = ['SelectionTo']


class SelectionTo(plugin.Plugin):

    capabilities = ['terminal_menu']
	
    def callback(self, menuitems, menu, terminal):
        """Add our menu items to the menu"""
        item = gtk.MenuItem(_('_Selection To'))

        # fire only if there is a selection
        if terminal.vte.get_has_selection():
            clip = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
            selection = clip.wait_for_text().strip()

            # we handle only numbers
            if selection.isdigit():
                # time durations
                time_submenu = gtk.Menu()
                time_submenu.append(self.gen_time_menu('From Millis', int(selection)))
                time_submenu.append(self.gen_time_menu('From Seconds', int(selection)*1000))
                item.set_submenu(time_submenu)
                menuitems.append(item)


    def gen_time_menu(self, title, value):

            submenu = gtk.Menu()
            from_x = gtk.MenuItem(_('_' + title))
            from_x.set_submenu(submenu)

            duration_str = gtk.MenuItem(_('_%s' % timedelta(milliseconds=value)))
            submenu.append(duration_str)

            d = datetime.fromtimestamp(value)
            date_str = gtk.MenuItem(_('_%s' % d.isoformat()))
            submenu.append(date_str)

            return from_x

