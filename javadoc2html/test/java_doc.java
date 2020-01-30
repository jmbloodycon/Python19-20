/** 
 * Класс продукции со свойствами <b>maker</b> и <b>price</b>.
 * @autor Киса Воробьянинов
 * @version 2.1
*/
class Product
{
    /** Поле производитель */
    private String maker;

    /** Поле цена */
    public double price;

    /** 
     * Конструктор - создание нового объекта
     * @see Product#Product(String, double)
     */
    Product()
    {
        setMaker("");
        price=0;
    }
}