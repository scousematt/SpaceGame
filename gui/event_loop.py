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


def move_panel(element, panel, pos,  game):
    if element.drag_with_mouse and element.rect.collidepoint(pos):
        game.lmb_pressed = True
        game.mouse_x = pos[0]
        game.mouse_y = pos[1]
        game.element_moving = panel
