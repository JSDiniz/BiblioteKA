from copies.models import Copy

def copyInventory(user, book):

    book_inv = Copy.objects.filter(book_id=book.id).filter(is_avaliable=True).first()

    if not book_inv:
        return {
        "title": "Livro Indisponível", 
        "mensagem": f"Olá {user.first_name} {user.last_name} o livro {book.name} não está disponível."}

    return {
        "title": "Livro Disponível", 
        "mensagem": f"Olá {user.first_name} {user.last_name} o livro {book.name} está disponível."}