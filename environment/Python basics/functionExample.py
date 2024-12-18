"""
This script demostrates the use of Python functions.
the create_shoe function takes a list fo materials as input and 
determines the type of the shoe created on those materials.
"""
def main():
    # Determina the shoe types based on the materials provided
    materials = [['leather', 'ruber'],['mesh', 'ruber'],['plastic', 'ruber']]
    
    # Use the create_shoe function and check the result
    shoes = []
    for material in materials:
        shoes.append(create_shoe(material))

    for shoe in shoes:
        if shoe['type'] == 'unknown':
            print(f"Unknown shoe type fo the given material: {shoe['materials']}")
        else:
            print(f"Shoe created of type: {shoe['type']}")
    
def create_shoe(material_list):
    shoe_type = ''
    
    if 'leather' in material_list and 'ruber' in material_list:
        shoe_type = 'boots'
    elif 'mesh' in material_list and 'ruber' in material_list:
        shoe_type = 'sneakers'
    else:
        shoe_type = 'unknown'
    
    return {'type' : shoe_type, 'materials' : material_list}
 
if __name__ == '__main__':
    main()