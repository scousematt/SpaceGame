import base_gui, labels

def button_clicked(element):
    element.on_click()

def treeview_clicked(element, pos):
    for child in element.children:
        if isinstance(child, base_gui.BUTTONS) and child.rect.collidepoint(pos):
            button_clicked(child)
            #  Now make the panel containing the treeview to changed.
            element.parent.changed = True
        if isinstance(child, labels.DefaultLabel) and child.get_text_surface().rect.collidepoint(pos):
            #  Clicked on a label within the treeview, the label contains a text_surface that has a rect
            print(child.text)


def move_panel(element, panel, pos,  gui):
    print(f'Event loop move panel clicked')
    panel.changed = True
    if element.drag_with_mouse and element.rect.collidepoint(pos):
        gui.lmb_pressed = True
        gui.mouse_x = pos[0]
        gui.mouse_y = pos[1]
        gui.element_moving = panel

def mouse_left_scrollbar(gui, element, pos):
    #  Mouse has left clicked on a scrollbars.Scrollbar
    gui.lmb_pressed = True
    # TODO change to vector2 to allow pos - mouse_clicked_pos
    gui.mouse_x = pos[0]
    gui.mouse_y = pos[1]
    # we want the scrollbar to update itself, not a scrollbar element
    gui.element_moving = element
