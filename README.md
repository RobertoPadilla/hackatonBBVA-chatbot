# Forecash-tin bot 🤖

Una forma sencilla y rápida para consultar los cajeros más cercanos.

**Unicamente saludame con un mensaje y yo te guiaré!** ⬇️

https://api.whatsapp.com/send?phone=14155238886

Por ser entorno de desarrollo se necesita un paso adicional: el cual es suscribirse al entorno de pruebas de nuestro chatbot. Simplemente su primer mensaje deberá ser esta cadena: `join fox-unless`.

### Recapitulando:
- **Primer paso:** enviar `join fox-unless` al chat-bot https://api.whatsapp.com/send?phone=14155238886
- **Segundo paso:** saludar al bot 👋🏽

---

## Funcionamiento
Soy un bot entrenado para el analizis de disponibilidad de los cajeros BBVA, evitando largas filas o traslados innecesarios a sucursales que no estén operando correctamente.

Mi motor de lenguaje es `DialogFlow`, el cual me entrenó para saber contestar a las personas!

El servicio de mensajería que utilizo es `twilio`, así podemos interactuar las veces que tu lo necesites.

Todo esto comprendido dentro de una API construida en python ayudandonos del framework `Flask` que facilita la integración de todas estas tecnologías.

Para la obtención de tráfico se utilizó la API de `Distance Matrix de Google`