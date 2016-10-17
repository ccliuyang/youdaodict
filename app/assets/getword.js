YoudaoGetWord = {
	mouseX: 0,
	mouseY: 0,
	bDrag: false,
	init: function () {
		self = this;
	    document.addEventListener("mousemove", function (e) {
			self.mouseX = e.clientX;
			self.mouseY = e.clientY;
		});
		window.addEventListener("mouseout", function (e) {
			self.mouseX = 0;
			self.mouseY = 0;			
		});
		document.addEventListener("mousedown", function() {
			self.bDrag = true;
		});
		document.addEventListener("mouseup", function() {
			if (self.bDrag && YoudaoGetWord_State && YoudaoGetWord_State.wordstroke) {
				self.bDrag = false;
				var sel = window.getSelection();
				if (sel.rangeCount > 0) {
					var txt = sel.getRangeAt(0).toString();
					if (txt.length > 0) {
						external.cppCall("onWordStroke", txt);
					}
				}
			}
		});		
	},
	getWord: function () {
		var ret = { text: "", pos: -1};
		if (this.mouseX  == 0 || this.mouseY == 0) {
			return ret;
		}
		var r = document.caretRangeFromPoint(this.mouseX, this.mouseY);
		if (!r) {
			return ret;
		}
		if (r.startContainer.data) {
			var rcText = null;
			if (r.startContainer.getBoundingClientRect) {
				rcText = r.startContainer.getBoundingClientRect();
			} else if (r.startContainer.parentElement && r.startContainer.parentElement.getBoundingClientRect) {
				rcText = r.startContainer.parentElement.getBoundingClientRect();
			}
			if (rcText == null || (rcText && rcText.left < this.mouseX && this.mouseX < rcText.right && rcText.top < this.mouseY && this.mouseY < rcText.bottom)) {
				ret.text = r.startContainer.data;
				ret.pos = r.startOffset;
				return ret;
			}
		}
		return ret;
	}
}
YoudaoGetWord.init();