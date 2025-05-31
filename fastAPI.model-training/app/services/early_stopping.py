class EarlyStopping:
    """Early stopping to stop training when validation loss does not
    improve."""

    def __init__(self, patience=3, min_delta=0.0):
        """Initializes the EarlyStopping instance.

        :param patience: How many epochs to wait for improvement before
            stopping.
        :param min_delta: Minimum change in the monitored quantity to
            qualify as an improvement.
        """
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False

    def __call__(self, val_loss):
        """Call method to check if early stopping should be triggered.

        :param val_loss: Validation loss to monitor.
        :return: None
        """
        if (
            self.best_loss is None
            or val_loss < self.best_loss - self.min_delta
        ):
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
