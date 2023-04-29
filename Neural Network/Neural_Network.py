from data import get_mnist
import numpy as np
import matplotlib.pyplot as plt

images, labels = get_mnist()
learn_rate = 0.03
epochs = 6
batch_size = 5


def activation(input):
    output = 1 / (1 + np.exp(-input))
    return output


def activation_derivate(input):
    output = (input * (1 - input))
    return output


class Layer:

    def __init__(self, no_of_inputs, no_of_nodes):
        self.no_of_inputs = no_of_inputs
        self.no_of_nodes = no_of_nodes
        self.weights = np.random.uniform(-0.5, 0.5, (self.no_of_nodes, self.no_of_inputs))
        self.bias = np.zeros((self.no_of_nodes, 1))
        self.delta_weights = np.zeros((self.no_of_nodes, self.no_of_inputs))
        self.delta_bias = np.zeros((self.no_of_nodes, 1))
        self.input = None
        self.output = None
        self.delta_loss = None

    def reset_delta(self):
        self.delta_weights = np.zeros((self.no_of_nodes, self.no_of_inputs))
        self.delta_bias = np.zeros((self.no_of_nodes, 1))

    def forward_pass(self, input):
        self.input = input
        weighted_sum = self.bias + self.weights @ self.input
        self.output = activation(weighted_sum)
        return self.output

    def backward_pass(self, learning_rate, next_delta_loss):
        self.delta_weights += -learning_rate * next_delta_loss @ np.transpose(self.input)
        self.delta_bias += -learning_rate * next_delta_loss
        self.delta_loss = np.transpose(self.weights) @ next_delta_loss * activation_derivate(self.input)
        return self.delta_loss

    def update_parameters(self, batch_size):
        self.weights += (self.delta_weights / batch_size)
        self.bias += (self.delta_bias / batch_size)
        self.reset_delta()


class NeuralNetwork:

    def __init__(self, list_of_nodes, batch_size, learning_rate):
        self.list_of_nodes = list_of_nodes
        self.no_of_input_nodes = self.list_of_nodes[0]
        self.no_of_layers = len(self.list_of_nodes)
        self.no_of_hidden_layers = self.no_of_layers - 1
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.layers = list()
        for i in range(1, self.no_of_layers):
            layer = Layer(self.list_of_nodes[i-1], self.list_of_nodes[i])
            self.layers.append(layer)
        self.input = None
        self.output = None

    def forward_propagation(self, input):
        self.input = input
        for i in range(0, self.no_of_hidden_layers):
            input = self.layers[i].forward_pass(input)
        self.output = input
        return self.output

    def calculate_loss(self, label):
        loss = self.output - label
        return loss

    def update_parameters(self):
        for i in range(0, self.no_of_hidden_layers):
            self.layers[i].update_parameters(self.batch_size)

    def backward_propagation(self, loss):
        for i in range(self.no_of_hidden_layers - 1, -1, -1):
            loss = self.layers[i].backward_pass(self.learning_rate, loss)

    def train_network(self):
        iteration = 0
        for epoch in range(epochs):
            nr_correct = 0
            for image, label in zip(images, labels):
                image.shape += (1,)
                label.shape += (1,)
                self.forward_propagation(image)
                nr_correct += int(np.argmax(self.output) == np.argmax(label))
                loss = self.calculate_loss(label)
                self.backward_propagation(loss)
                iteration += 1
                if iteration % batch_size == 0:
                    self.update_parameters()
            print(f"Acc: {round((nr_correct / images.shape[0]) * 100, 2)}%")

    def test_network(self):
        while True:
            try:
                index = int(input("Enter test image index: (0 - 59999): "))
                img = images[index]
                plt.imshow(img.reshape(28, 28), cmap="Greys")
                img.shape += (1,)
                output = self.forward_propagation(img)
                plt.title(f"Predicted Digit: {output.argmax()} :)")
                plt.show(block=False)
                plt.pause(3)
                plt.close()
            except Exception:
                break


if __name__ == '__main__':
    nn = NeuralNetwork([784, 40, 40, 10], batch_size, learn_rate)
    nn.train_network()
    nn.test_network()
