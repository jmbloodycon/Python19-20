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

    /** 
     * Конструктор - создание нового объекта с определенными значениями
     * @param maker - производитель
     * @param price - цена
     * @see Product#Product()
     */
    Product(String maker,double price){
        this.setMaker(maker);
        this.price=price;
    }

    /**
     * Функция получения значения поля {@link Product#maker}
     * @return возвращает название производителя
     */
    public String getMaker() {
        return maker;
    }

   /**
     * Процедура определения производителя {@link Product#maker}
     * @param maker - производитель
     */
    public void setMaker(String maker) {
        this.maker = maker;
    }
}