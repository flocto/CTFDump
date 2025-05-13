extends Area2D

@onready var timer = $Timer

func _on_body_entered(body):
	Engine.time_scale = 2
	body.get_node("CollisionShape2D").queue_free()
	timer.start()


func _on_timer_timeout():
	Engine.time_scale = 1
	Globals.death += 1
	get_tree().reload_current_scene()
