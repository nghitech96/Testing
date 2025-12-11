from keras.models import Model
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, Flatten


# Tạo đầu vào cho mô hình
input_layer = Input(shape=(100, 50, 1))

# Tạo lớp ẩn cho mô hình
hidden_layer = Conv2D(32, (3, 3), activation='relu')(input_layer)
hidden_layer = MaxPooling2D((2, 2))(hidden_layer)
hidden_layer = Flatten()(hidden_layer)
hidden_layer = Dense(64, activation='relu')(hidden_layer)

# Tạo đầu ra cho nhiệm vụ 1
output_layer_task1 = Dense(2, activation='softmax')(hidden_layer)

# Tạo đầu ra cho nhiệm vụ 2
output_layer_task2 = Dense(10, activation='softmax')(hidden_layer)

# Tạo mô hình MTL
model = Model(inputs=input_layer, outputs=[output_layer_task1, output_layer_task2])

model.compile(optimizer='adam', loss=['sparse_categorical_crossentropy', 'sparse_categorical_crossentropy'], metrics=['accuracy'])

model.fit(X_train, [y_train_task1, y_train_task2], epochs=10, batch_size=128, validation_data=(X_test, [y_test_task1, y_test_task2]))

loss_task1, accuracy_task1, loss_task2, accuracy_task2 = model.evaluate(X_test, [y_test_task1, y_test_task2])
print(f'Độ chính xác nhiệm vụ 1: {accuracy_task1:.2f}%')
print(f'Độ chính xác nhiệm vụ 2: {accuracy_task2:.2f}%')