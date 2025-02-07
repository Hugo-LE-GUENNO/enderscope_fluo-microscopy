{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2dc8d2cb-87c9-4a07-bd90-1cc05a0a88b4",
   "metadata": {},
   "outputs": [],
   "source": [
    "class EnderTemp:\n",
    "    def __init__(self):\n",
    "        self.temperature = 20.0\n",
    "\n",
    "    def get_controls(self):\n",
    "        temperature_slider = widgets.FloatSlider(\n",
    "            value=self.temperature,\n",
    "            min=-30.0,\n",
    "            max=50.0,\n",
    "            step=0.1,\n",
    "            description='Temperature (°C):',\n",
    "            continuous_update=True,\n",
    "            style={'description_width': 'initial'}\n",
    "        )\n",
    "\n",
    "        def update_temperature(change):\n",
    "            self.temperature = change['new']\n",
    "\n",
    "        temperature_slider.observe(update_temperature, names='value')\n",
    "\n",
    "        return widgets.VBox([temperature_slider])\n",
    "\n",
    "    def get_output(self):\n",
    "        return widgets.Label(value=f\"Current Temperature: {self.temperature:.1f} °C\")\n",
    "\n",
    "    def has_output(self):\n",
    "        return False"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
