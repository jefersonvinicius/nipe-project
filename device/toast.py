from plyer import notification


class Toast:

    @staticmethod
    def show(message):
        notification.notify(message=message, toast=True)